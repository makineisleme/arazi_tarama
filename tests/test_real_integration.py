from terrain_scan_agent.gps_imu_driver import GPSIMUDriver
from terrain_scan_agent.px4_controller import PX4Controller
from terrain_scan_agent.real_camera import RealCameraReader


def test_gps_imu_driver_supports_live_configuration():
    driver = GPSIMUDriver(
        lat=41.012,
        lon=28.978,
        altitude_m=12.5,
        source="serial:///dev/ttyUSB0",
        mode="live",
    )
    state = driver.read()

    assert state["status"] == "ok"
    assert state["mode"] == "live"
    assert state["source"] == "serial:///dev/ttyUSB0"
    assert state["position"]["lat"] == 41.012
    assert state["position"]["altitude_m"] == 12.5


def test_px4_controller_accepts_string_commands():
    controller = PX4Controller(vehicle="drone")
    result = controller.send_commands(["arm", "takeoff", "move"])

    assert result["status"] == "ok"
    assert result["vehicle"] == "drone"
    assert result["safe"] is True
    assert [item["command"] for item in result["commands"]] == ["arm", "takeoff", "move"]


def test_real_camera_reader_accepts_configured_source():
    camera = RealCameraReader(sensor_name="front_cam", source="/dev/video0")
    frame = camera.read_frame()

    assert frame["sensor"] == "front_cam"
    assert frame["source"] == "/dev/video0"
    assert "frame_id" in frame
    assert frame["status"] in {"ok", "fallback"}
