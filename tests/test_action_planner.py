from terrain_scan_agent.planner import build_action_plan, generate_vehicle_commands


def test_build_action_plan_for_scan_task():
    plan = build_action_plan("Bu arazide tarama yap ve riskli alanları bul")

    assert plan[0]["action"] == "scan_area"
    assert "capture_frames" in {step["action"] for step in plan}
    assert "analyze_results" in {step["action"] for step in plan}


def test_generate_vehicle_commands_for_drone():
    plan = build_action_plan("Drone ile 3 metre yükseklikte tarama yap")
    commands = generate_vehicle_commands(plan, vehicle="drone")

    assert "takeoff" in commands
    assert "move_to_waypoint" in commands
    assert "start_scan" in commands
    assert "return_home" in commands


def test_safe_mission_execution_for_drone():
    from terrain_scan_agent.mission import create_mission

    mission = create_mission(
        "Arazide riskli alanları bul ve tarama yap",
        vehicle="drone",
        altitude_m=3,
        safety_margin_m=5,
    )

    assert mission["status"] == "safe"
    assert mission["vehicle"] == "drone"
    assert mission["plan"][0]["action"] == "scan_area"
    assert "takeoff" in mission["commands"]
    assert "return_home" in mission["commands"]


def test_robot_mission_uses_robot_commands():
    from terrain_scan_agent.mission import create_mission

    mission = create_mission(
        "Robot ile arazi çevresini tara",
        vehicle="robot",
        altitude_m=0,
        safety_margin_m=2,
    )

    assert mission["vehicle"] == "robot"
    assert "start_navigation" in mission["commands"]
    assert mission["status"] == "safe"


def test_sensor_registry_collects_expected_devices():
    from terrain_scan_agent.sensors import SensorManager

    manager = SensorManager()
    manager.register("camera", "rgb")
    manager.register("gps", "gnss")
    manager.register("imu", "imu")

    assert manager.active_names() == ["camera", "gps", "imu"]
    assert manager.summary()["count"] == 3


def test_perception_detects_risk_on_dense_scan():
    from terrain_scan_agent.vision import analyze_scan

    result = analyze_scan({"annotations": ["obstacle", "obstacle", "obstacle", "anomaly"]})

    assert result["risk_level"] == "high"
    assert result["detected_objects"] >= 3


def test_control_layer_executes_command_sequence():
    from terrain_scan_agent.control import Controller

    controller = Controller(vehicle="drone")
    result = controller.execute(["takeoff", "move_to_waypoint", "start_scan"])

    assert result["status"] == "ok"
    assert result["executed"] == ["takeoff", "move_to_waypoint", "start_scan"]


def test_safety_gate_rejects_unsafe_mission():
    from terrain_scan_agent.safety import SafetyManager

    safety = SafetyManager(vehicle="drone")
    result = safety.check(altitude_m=50, clearance_m=1)

    assert result["safe"] is False
    assert "altitude" in result["reason"].lower()


def test_ros_bridge_dispatches_drone_commands():
    from terrain_scan_agent.ros_bridge import ROSBridge

    bridge = ROSBridge(vehicle="drone")
    result = bridge.dispatch(["takeoff", "move_to_waypoint", "start_scan"])

    assert result["status"] == "ok"
    assert result["vehicle"] == "drone"
    assert result["published"] == ["takeoff", "move_to_waypoint", "start_scan"]


def test_robot_adapter_uses_navigation_commands():
    from terrain_scan_agent.robot_adapter import RobotAdapter

    adapter = RobotAdapter()
    result = adapter.send("start_navigation")

    assert result["status"] == "ok"
    assert result["command"] == "start_navigation"
    assert result["vehicle"] == "robot"


def test_mavlink_adapter_dispatches_drone_commands():
    from terrain_scan_agent.mavlink_adapter import MAVLinkAdapter

    adapter = MAVLinkAdapter(vehicle="drone")
    result = adapter.dispatch(["arm", "takeoff", "waypoint"])

    assert result["status"] == "ok"
    assert result["vehicle"] == "drone"
    assert result["published"] == ["arm", "takeoff", "waypoint"]


def test_topic_controller_publishes_mission_topics():
    from terrain_scan_agent.topic_controller import TopicController

    controller = TopicController(vehicle="drone")
    result = controller.publish_batch("mission", ["scan_area", "capture_frames"])

    assert result["status"] == "ok"
    assert result["vehicle"] == "drone"
    assert result["payloads"] == ["scan_area", "capture_frames"]


def test_sensor_stream_tracks_capture_payloads():
    from terrain_scan_agent.sensor_stream import SensorStream

    stream = SensorStream("camera")
    stream.capture({"frame": 1, "risk": "normal"})
    stream.capture({"frame": 2, "risk": "obstacle"})

    snapshot = stream.snapshot()
    assert snapshot["sensor"] == "camera"
    assert snapshot["count"] == 2
    assert snapshot["alerts"] == 1


def test_processing_pipeline_aggregates_telemetry():
    from terrain_scan_agent.processor import ProcessingPipeline

    pipeline = ProcessingPipeline()
    summary = pipeline.process(
        {
            "camera": [{"frame": 1, "risk": "normal"}, {"frame": 2, "risk": "obstacle"}],
            "gps": [{"lat": 39.0, "lon": 35.0}],
            "imu": [{"yaw": 10.0, "pitch": 2.0}],
        }
    )

    assert summary["total_frames"] == 2
    assert summary["risk_events"] == 1
    assert summary["status"] == "active"


def test_camera_capture_tracks_frames():
    from terrain_scan_agent.camera_capture import CameraCapture

    camera = CameraCapture("front_cam")
    camera.capture({"frame_id": 1, "risk": "normal"})
    camera.capture({"frame_id": 2, "risk": "obstacle"})

    state = camera.state()
    assert state["sensor"] == "front_cam"
    assert state["frame_count"] == 2
    assert state["risk_count"] == 1


def test_sensor_fusion_combines_camera_lidar_and_gps():
    from terrain_scan_agent.sensor_fusion import SensorFusion

    fusion = SensorFusion()
    result = fusion.combine(
        {
            "camera": [{"frame_id": 1, "risk": "obstacle"}],
            "lidar": [{"distance_m": 1.2, "obstacle": True}],
            "gps": [{"lat": 39.0, "lon": 35.0}],
        }
    )

    assert result["status"] == "active"
    assert result["frame_count"] == 1
    assert result["obstacle_detected"] is True
    assert result["gps_points"] == 1
