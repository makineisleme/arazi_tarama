from terrain_scan_agent.camera_capture import CameraCapture
from terrain_scan_agent.control import Controller
from terrain_scan_agent.mission import create_mission
from terrain_scan_agent.processor import ProcessingPipeline
from terrain_scan_agent.sensor_fusion import SensorFusion
from terrain_scan_agent.sensor_stream import SensorStream
from terrain_scan_agent.sensors import SensorManager
from terrain_scan_agent.ui import render_summary
from terrain_scan_agent.vision import analyze_scan


def main() -> None:
    user_prompt = "Bu arazide tarama yap ve riskli alanları bul"
    mission = create_mission(
        user_prompt,
        vehicle="drone",
        altitude_m=3,
        safety_margin_m=5,
    )

    sensor_manager = SensorManager()
    sensor_manager.register("camera", "rgb")
    sensor_manager.register("gps", "gnss")
    sensor_manager.register("imu", "imu")
    sensor_manager.register("lidar", "lidar")

    camera_stream = SensorStream("camera")
    camera_stream.capture({"frame": 1, "risk": "normal"})
    camera_stream.capture({"frame": 2, "risk": "obstacle"})

    camera_capture = CameraCapture("front_cam")
    camera_capture.capture({"frame_id": 1, "risk": "obstacle"})

    controller = Controller(vehicle="drone")
    command_result = controller.execute(mission["commands"])
    scan_result = analyze_scan({"annotations": ["obstacle", "obstacle", "obstacle", "anomaly"]})
    pipeline_result = ProcessingPipeline().process({
        "camera": camera_stream.snapshot()["samples"],
        "gps": [{"lat": 39.0, "lon": 35.0}],
        "imu": [{"yaw": 10.0, "pitch": 2.0}],
    })
    fusion_result = SensorFusion().combine({
        "camera": camera_capture.state()["frames"],
        "lidar": [{"distance_m": 1.2, "obstacle": True}],
        "gps": [{"lat": 39.0, "lon": 35.0}],
    })

    print(render_summary(mission))
    print("\nSensors:")
    for sensor in sensor_manager.summary()["sensors"]:
        print(f"- {sensor['name']} ({sensor['kind']})")

    print("\nController:")
    print(command_result)

    print("\nPerception:")
    print(scan_result)

    print("\nTelemetry processing:")
    print(pipeline_result)

    print("\nSensor fusion:")
    print(fusion_result)


if __name__ == "__main__":
    main()
