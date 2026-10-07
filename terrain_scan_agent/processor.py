from __future__ import annotations

from typing import Any, Dict, List


class ProcessingPipeline:
    """Aggregates sensor data and computes a simple operational summary."""

    def process(self, sensor_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        camera_frames = sensor_data.get("camera", [])
        gps_points = sensor_data.get("gps", [])
        imu_points = sensor_data.get("imu", [])
        lidar_points = sensor_data.get("lidar", [])

        total_frames = len(camera_frames)
        risk_events = sum(1 for frame in camera_frames if frame.get("risk") == "obstacle")
        lidar_obstacles = sum(
            1 for point in lidar_points if point.get("obstacle") is True or float(point.get("distance_m", 999.0)) <= 1.5
        )

        return {
            "status": "active",
            "total_frames": total_frames,
            "risk_events": risk_events + lidar_obstacles,
            "gps_points": len(gps_points),
            "imu_points": len(imu_points),
            "lidar_points": len(lidar_points),
            "summary": "Telemetry processed successfully.",
        }
