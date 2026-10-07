from terrain_scan_agent.control import Controller
from terrain_scan_agent.field_runtime import FieldRuntime
from terrain_scan_agent.mission import create_mission
from terrain_scan_agent.processor import ProcessingPipeline
from terrain_scan_agent.reporting import build_report, save_report, save_report_text
from terrain_scan_agent.risk_map import build_risk_map, render_risk_map
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

    runtime = FieldRuntime(vehicle="drone", camera_name="front_cam", camera_source=0, gps_mode="simulated")
    runtime_result = runtime.run_scan(user_prompt, altitude_m=3.0, safety_margin_m=5.0)

    controller = Controller(vehicle="drone")
    command_result = controller.execute(mission["commands"])
    scan_result = analyze_scan({"annotations": ["obstacle", "obstacle", "obstacle", "anomaly"]})
    pipeline_result = ProcessingPipeline().process({
        "camera": camera_stream.snapshot()["samples"],
        "gps": [{"lat": 39.0, "lon": 35.0}],
        "imu": [{"yaw": 10.0, "pitch": 2.0}],
    })
    fusion_result = SensorFusion().combine({
        "camera": [{"frame_id": 1, "risk": "obstacle"}],
        "lidar": [{"distance_m": 1.2, "obstacle": True}],
        "gps": [{"lat": 39.0, "lon": 35.0}],
    })
    risk_map = build_risk_map([
        {"x": 1, "y": 1, "risk": "high", "label": "obstacle"},
        {"x": 2, "y": 3, "risk": "medium", "label": "anomaly"},
        {"x": 5, "y": 5, "risk": "low", "label": "clear"},
    ], width=8, height=8)

    print(render_summary(mission))
    print("\nSensors:")
    for sensor in sensor_manager.summary()["sensors"]:
        print(f"- {sensor['name']} ({sensor['kind']})")

    print("\nField runtime:")
    print(runtime_result)

    print("\nController:")
    print(command_result)

    print("\nPerception:")
    print(scan_result)

    print("\nTelemetry processing:")
    print(pipeline_result)

    print("\nSensor fusion:")
    print(fusion_result)

    print("\nRisk map:")
    print(render_risk_map(risk_map))

    report = build_report(mission, runtime_result, scan_result, fusion_result, risk_map)
    report_file = save_report(report)
    text_file = save_report_text(report)
    print(f"\nReport saved to: {report_file}")
    print(f"Summary saved to: {text_file}")


if __name__ == "__main__":
    main()
