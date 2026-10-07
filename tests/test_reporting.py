from terrain_scan_agent.reporting import build_report, save_report, save_report_text


def test_build_report_includes_runtime_and_risk_summary(tmp_path):
    mission = {
        "status": "safe",
        "vehicle": "drone",
        "summary": "Mission complete",
        "plan": [{"action": "scan_area"}, {"action": "capture_frames"}],
        "commands": ["takeoff", "scan_area"],
    }
    runtime = {"status": "safe", "camera": {"sensor": "front_cam"}, "flight": {"status": "ok"}}
    scan = {"risk_level": "high", "detected_objects": 3, "summary": "High risk"}
    fusion = {"status": "active", "obstacle_detected": True}
    risk_map = {"status": "ok", "risk_score": 0.8, "max_risk": 0.9, "hotspots": [{"x": 1, "y": 1, "risk": 0.9}], "summary": "High risk detected"}

    report = build_report(mission, runtime, scan, fusion, risk_map)

    assert report["status"] == "safe"
    assert report["perception"]["risk_level"] == "high"
    assert report["risk_map"]["risk_score"] == 0.8
    assert report["plan"]["count"] == 2

    json_path = save_report(report, directory=str(tmp_path))
    text_path = save_report_text(report, directory=str(tmp_path), filename="mission_summary.txt")

    assert json_path.exists()
    assert text_path.exists()
    assert "takeoff" in text_path.read_text(encoding="utf-8")
