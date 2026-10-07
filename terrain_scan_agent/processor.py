from __future__ import annotations

from typing import Any, Dict, List


class ProcessingPipeline:
    """Aggregates sensor data and computes a simple operational summary."""

    def process(self, sensor_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        camera_frames = sensor_data.get("camera", [])
        gps_points = sensor_data.get("gps", [])
        imu_points = sensor_data.get("imu", [])

        total_frames = len(camera_frames)
        risk_events = sum(1 for frame in camera_frames if frame.get("risk") == "obstacle")

        return {
            "status": "active",
            "total_frames": total_frames,
            "risk_events": risk_events,
            "gps_points": len(gps_points),
            "imu_points": len(imu_points),
            "summary": "Telemetry processed successfully.",
        }
