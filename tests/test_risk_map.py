from terrain_scan_agent.risk_map import build_risk_map, render_risk_map


def test_build_risk_map_converts_obstacles_to_grid():
    risk_map = build_risk_map(
        [
            {"x": 1, "y": 1, "risk": "high", "label": "obstacle"},
            {"x": 2, "y": 2, "risk": "medium", "label": "anomaly"},
            {"x": 5, "y": 5, "risk": "low", "label": "clear"},
        ],
        width=6,
        height=6,
    )

    assert risk_map["status"] == "ok"
    assert risk_map["width"] == 6
    assert risk_map["height"] == 6
    assert risk_map["max_risk"] >= 0.8
    assert any(item["label"] == "obstacle" for item in risk_map["hotspots"])
    assert "risk" in risk_map["summary"].lower()


def test_render_risk_map_returns_readable_ascii_summary():
    risk_map = build_risk_map([{"x": 0, "y": 0, "risk": "high"}], width=2, height=2)
    ascii_map = render_risk_map(risk_map)

    assert "Risk Map" in ascii_map
    assert "Summary:" in ascii_map
    assert "H" in ascii_map
