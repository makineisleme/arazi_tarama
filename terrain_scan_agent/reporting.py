from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


def build_report(
    mission: Dict[str, Any],
    runtime_result: Optional[Dict[str, Any]] = None,
    scan_result: Optional[Dict[str, Any]] = None,
    fusion_result: Optional[Dict[str, Any]] = None,
    risk_map: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build a normalized mission report that can be saved to JSON or served by the dashboard."""
    runtime_result = runtime_result or {}
    scan_result = scan_result or {}
    fusion_result = fusion_result or {}
    risk_map = risk_map or {}

    risk_level = scan_result.get("risk_level", "unknown")
    risk_score = risk_map.get("risk_score", 0.0)
    hotspots = risk_map.get("hotspots", [])
    max_risk = risk_map.get("max_risk", 0.0)

    report = {
        "status": mission.get("status", "unknown"),
        "vehicle": mission.get("vehicle", "drone"),
        "summary": mission.get("summary", "Mission completed."),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "plan": {
            "count": len(mission.get("plan", [])),
            "actions": [step.get("action", "unknown") for step in mission.get("plan", [])],
        },
        "commands": mission.get("commands", []),
        "runtime": {
            "status": runtime_result.get("status", "unknown"),
            "camera": runtime_result.get("camera", {}),
            "flight": runtime_result.get("flight", {}),
            "controller": runtime_result.get("controller", {}),
        },
        "perception": {
            "risk_level": risk_level,
            "detected_objects": scan_result.get("detected_objects", 0),
            "summary": scan_result.get("summary", "No perception summary"),
        },
        "fusion": fusion_result,
        "risk_map": {
            "status": risk_map.get("status", "unknown"),
            "risk_score": risk_score,
            "max_risk": max_risk,
            "hotspot_count": len(hotspots),
            "summary": risk_map.get("summary", "No risk-map summary available."),
        },
    }

    if report["status"] == "safe":
        report["summary"] = f"{report['vehicle']} mission completed safely with {report['plan']['count']} plan steps."

    return report


def save_report(report: Dict[str, Any], directory: str = "artifacts", filename: str = "mission_report.json") -> Path:
    output_dir = Path(directory)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def save_report_text(report: Dict[str, Any], directory: str = "artifacts", filename: str = "mission_summary.txt") -> Path:
    output_dir = Path(directory)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    lines = [
        f"Status: {report.get('status', 'unknown')}",
        f"Vehicle: {report.get('vehicle', 'drone')}",
        f"Summary: {report.get('summary', 'Mission complete')}",
        f"Risk level: {report.get('perception', {}).get('risk_level', 'unknown')}",
        f"Risk score: {report.get('risk_map', {}).get('risk_score', 0.0)}",
        "Commands:",
    ]
    for command in report.get("commands", []):
        lines.append(f"- {command}")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path
