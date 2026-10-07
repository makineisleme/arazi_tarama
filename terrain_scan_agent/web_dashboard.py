from __future__ import annotations

import argparse
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlsplit, urlunsplit

from .dashboard import build_dashboard_html
from .live_camera import LiveCameraCapture


class CameraFrameStream:
    """Capture and JPEG-encode frames once for all connected dashboard clients."""

    def __init__(
        self,
        source: int | str,
        *,
        fallback: bool = True,
        fps: float = 8.0,
        jpeg_quality: int = 80,
    ) -> None:
        self.source = source
        self.fallback = fallback
        self.fps = max(0.5, fps)
        self.jpeg_quality = max(1, min(100, jpeg_quality))
        self._condition = threading.Condition()
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._reader: Optional[LiveCameraCapture] = None
        self._latest_jpeg: Optional[bytes] = None
        self._sequence = 0
        self._camera_state: Dict[str, Any] = {
            "source": source,
            "status": "connecting",
            "frame_id": 0,
        }
        self._error: Optional[str] = None

    def start(self) -> None:
        with self._condition:
            if self._thread is not None:
                return
            self._thread = threading.Thread(
                target=self._capture_loop,
                name="terrain-scan-camera-stream",
                daemon=True,
            )
            self._thread.start()

    def _capture_loop(self) -> None:
        try:
            import cv2  # type: ignore
            import numpy as np  # type: ignore

            self._reader = LiveCameraCapture(
                "dashboard_camera",
                source=self.source,
                fallback=self.fallback,
            )
            frame_interval = 1.0 / self.fps

            while not self._stop.is_set():
                started_at = time.monotonic()
                capture = self._reader.capture_frame()
                frame = capture.get("frame")
                if frame is None:
                    if not self.fallback:
                        raise RuntimeError("Camera is unavailable and fallback is disabled.")
                    frame = np.zeros((480, 640, 3), dtype=np.uint8)
                    cv2.putText(
                        frame,
                        "Camera unavailable - fallback mode",
                        (24, 240),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (230, 230, 230),
                        2,
                        cv2.LINE_AA,
                    )

                encoded, jpeg = cv2.imencode(
                    ".jpg",
                    frame,
                    [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality],
                )
                if not encoded:
                    raise RuntimeError("OpenCV failed to encode a camera frame as JPEG.")

                with self._condition:
                    self._sequence += 1
                    self._latest_jpeg = jpeg.tobytes()
                    self._camera_state = {
                        "source": self.source,
                        "status": capture.get("status", "fallback"),
                        "frame_id": capture.get("frame_id", self._sequence),
                        "timestamp": capture.get("timestamp"),
                        "shape": capture.get("shape"),
                    }
                    self._condition.notify_all()

                remaining = frame_interval - (time.monotonic() - started_at)
                if remaining > 0:
                    self._stop.wait(remaining)
        except Exception as error:
            with self._condition:
                self._error = str(error)
                self._camera_state = {
                    **self._camera_state,
                    "status": "error",
                    "error": self._error,
                }
                self._condition.notify_all()
        finally:
            if self._reader is not None:
                self._reader.close()

    def wait_for_frame(
        self,
        after_sequence: int,
        timeout: Optional[float] = None,
    ) -> Optional[Tuple[int, bytes]]:
        with self._condition:
            self._condition.wait_for(
                lambda: self._sequence > after_sequence or self._error is not None or self._stop.is_set(),
                timeout=timeout,
            )
            if self._sequence > after_sequence and self._latest_jpeg is not None:
                return self._sequence, self._latest_jpeg
            if self._error is not None and self._latest_jpeg is None:
                raise RuntimeError(self._error)
            return None

    def status(self) -> Dict[str, Any]:
        with self._condition:
            result = dict(self._camera_state)
            result["source"] = self._public_source()
            if self._error:
                result["error"] = self._error
            return result

    def _public_source(self) -> int | str:
        if not isinstance(self.source, str) or "://" not in self.source:
            return self.source
        parsed = urlsplit(self.source)
        if parsed.username is None and parsed.password is None and not parsed.query:
            return self.source
        safe_netloc = parsed.netloc.rsplit("@", 1)[-1]
        return urlunsplit(parsed._replace(netloc=safe_netloc, query="", fragment=""))

    @property
    def stopped(self) -> bool:
        return self._stop.is_set()

    def close(self) -> None:
        self._stop.set()
        with self._condition:
            self._condition.notify_all()
        if self._thread is not None:
            self._thread.join(timeout=2.0)


class DashboardRequestHandler(BaseHTTPRequestHandler):
    """Serve the dashboard, mission status, and a shared MJPEG camera stream."""

    server_version = "TerrainScanDashboard/1.0"

    def do_GET(self) -> None:  # noqa: N802 - handler interface
        path = urlsplit(self.path).path
        if path == "/api/status":
            self._send_json(self.server.get_dashboard_payload())
            return
        if path == "/stream.mjpg":
            self._serve_camera_stream()
            return
        if path == "/":
            html = build_dashboard_html(self.server.get_dashboard_payload())
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_error(404, "Not found")

    def _send_json(self, payload: Dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _serve_camera_stream(self) -> None:
        stream = self.server.camera_stream
        stream.start()
        try:
            first_frame = stream.wait_for_frame(after_sequence=0, timeout=5.0)
        except RuntimeError:
            self.send_error(503, "Camera stream unavailable")
            return
        if first_frame is None:
            self.send_error(503, "Camera stream did not produce a frame")
            return

        self.send_response(200)
        self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()

        sequence, jpeg = first_frame
        try:
            while True:
                self._write_frame(jpeg)
                next_frame = stream.wait_for_frame(after_sequence=sequence, timeout=2.0)
                if next_frame is None:
                    if stream.stopped or stream.status().get("status") == "error":
                        break
                    continue
                sequence, jpeg = next_frame
        except (BrokenPipeError, ConnectionResetError, OSError):
            return

    def _write_frame(self, jpeg: bytes) -> None:
        self.wfile.write(
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n"
            + f"Content-Length: {len(jpeg)}\r\n\r\n".encode("ascii")
            + jpeg
            + b"\r\n"
        )
        self.wfile.flush()

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return


class DashboardServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(
        self,
        server_address: Tuple[str, int],
        dashboard_payload: Dict[str, Any],
        *,
        camera_source: int | str = 0,
        camera_fallback: bool = True,
        fps: float = 8.0,
    ) -> None:
        self.dashboard_payload = dict(dashboard_payload)
        self._payload_lock = threading.RLock()
        self.camera_stream = CameraFrameStream(
            camera_source,
            fallback=camera_fallback,
            fps=fps,
        )
        super().__init__(server_address, DashboardRequestHandler)

    def get_dashboard_payload(self) -> Dict[str, Any]:
        with self._payload_lock:
            payload = dict(self.dashboard_payload)
        payload["camera"] = {
            **(payload.get("camera") or {}),
            **self.camera_stream.status(),
        }
        return payload

    def update_dashboard_payload(self, payload: Dict[str, Any]) -> None:
        with self._payload_lock:
            self.dashboard_payload = dict(payload)

    def server_close(self) -> None:
        self.camera_stream.close()
        super().server_close()


def run_dashboard_server(
    dashboard_payload: Optional[Dict[str, Any]] = None,
    *,
    host: str = "127.0.0.1",
    port: int = 8023,
    camera_source: int | str = 0,
    camera_fallback: bool = True,
    fps: float = 8.0,
) -> None:
    payload = dashboard_payload or {
        "status": "ok",
        "vehicle": "drone",
        "summary": "Dashboard ready.",
        "commands": ["scan_area", "capture_frames", "report"],
    }
    server = DashboardServer(
        (host, port),
        payload,
        camera_source=camera_source,
        camera_fallback=camera_fallback,
        fps=fps,
    )
    print(f"Dashboard running on http://{host}:{server.server_address[1]}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard shutting down.")
    finally:
        server.server_close()


def _parse_camera_source(value: str) -> int | str:
    return int(value) if value.isdigit() else value


def main() -> None:
    parser = argparse.ArgumentParser(description="Arazi tarama canlı web dashboard'u")
    parser.add_argument("--host", default="127.0.0.1", help="Dinlenecek adres (varsayılan: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8023, help="HTTP portu (varsayılan: 8023)")
    parser.add_argument(
        "--camera",
        type=_parse_camera_source,
        default=0,
        help="Kamera indeksi, cihaz yolu veya RTSP/HTTP URL'si (varsayılan: 0)",
    )
    parser.add_argument("--fps", type=float, default=8.0, help="Akış kare hızı")
    parser.add_argument(
        "--report",
        type=Path,
        help="Başlangıç dashboard verisi için JSON rapor dosyası",
    )
    parser.add_argument(
        "--no-camera-fallback",
        action="store_true",
        help="Kamera açılamazsa sentetik placeholder yayınlama",
    )
    args = parser.parse_args()
    payload = None
    if args.report is not None:
        payload = json.loads(args.report.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            parser.error("--report JSON dosyası bir nesne içermeli.")

    run_dashboard_server(
        dashboard_payload=payload,
        host=args.host,
        port=args.port,
        camera_source=args.camera,
        camera_fallback=not args.no_camera_fallback,
        fps=args.fps,
    )


if __name__ == "__main__":
    main()
