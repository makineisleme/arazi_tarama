import json
import threading
from urllib.error import HTTPError
from urllib.request import urlopen

import pytest

from terrain_scan_agent.dashboard import build_dashboard_html
from terrain_scan_agent.web_dashboard import DashboardServer


def test_build_dashboard_html_contains_dashboard_sections():
    html = build_dashboard_html({
        "status": "safe",
        "vehicle": "drone",
        "summary": "Mission ready",
        "commands": ["takeoff", "scan_area"],
    })

    assert "Arazi Tarama Dashboard" in html
    assert "safe" in html
    assert "takeoff" in html
    assert "/stream.mjpg" in html
    assert "/api/status" in html


def test_build_dashboard_html_escapes_user_supplied_content():
    html = build_dashboard_html({
        "status": "safe",
        "vehicle": "<script>alert(1)</script>",
        "summary": "<img src=x onerror=alert(1)>",
    })

    assert "<script>alert(1)</script>" not in html
    assert "<img src=x onerror=alert(1)>" not in html


def test_dashboard_server_stores_payload():
    server = DashboardServer(("127.0.0.1", 0), {"status": "ok", "vehicle": "robot"})

    assert server.dashboard_payload["vehicle"] == "robot"
    assert server.server_address[1] >= 0
    server.server_close()


@pytest.fixture
def running_dashboard():
    server = DashboardServer(
        ("127.0.0.1", 0),
        {"status": "safe", "vehicle": "drone", "summary": "Test mission"},
        camera_source=999,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_dashboard_http_routes_serve_live_html_and_status(running_dashboard):
    with urlopen(running_dashboard + "/") as response:
        html = response.read().decode("utf-8")
        assert response.status == 200
        assert "Canlı kamera" in html
        assert "/stream.mjpg" in html

    with urlopen(running_dashboard + "/api/status") as response:
        payload = json.load(response)
        assert response.status == 200
        assert payload["vehicle"] == "drone"
        assert payload["camera"]["status"] == "connecting"


def test_dashboard_http_routes_return_404_for_unknown_paths(running_dashboard):
    with pytest.raises(HTTPError) as error:
        urlopen(running_dashboard + "/not-a-route")

    assert error.value.code == 404


def test_dashboard_stream_returns_mjpeg_frames(running_dashboard):
    with urlopen(running_dashboard + "/stream.mjpg", timeout=5) as response:
        assert response.status == 200
        assert response.headers["Content-Type"].startswith(
            "multipart/x-mixed-replace; boundary=frame"
        )
        assert response.readline() == b"--frame\r\n"
        assert response.readline().lower().startswith(b"content-type: image/jpeg")
        length_header = response.readline().decode("ascii")
        frame_length = int(length_header.split(":", 1)[1].strip())
        assert response.readline() == b"\r\n"
        jpeg = response.read(frame_length)

    assert jpeg.startswith(b"\xff\xd8")
    assert jpeg.endswith(b"\xff\xd9")


def test_dashboard_status_redacts_camera_url_credentials():
    server = DashboardServer(
        ("127.0.0.1", 0),
        {},
        camera_source="rtsp://operator:secret@camera.local/live?token=hidden",
    )

    try:
        camera_status = server.get_dashboard_payload()["camera"]
    finally:
        server.server_close()

    assert camera_status["source"] == "rtsp://camera.local/live"
    assert "secret" not in str(camera_status)
    assert "hidden" not in str(camera_status)
