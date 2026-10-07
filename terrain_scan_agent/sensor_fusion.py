from __future__ import annotations

from typing import Any, Dict, List


class SensorFusion:
    """Combines camera, GPS, and LiDAR data for a simple fused scan state."""

    def combine(self, sensor_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        camera_frames = sensor_data.get("camera", [])
        lidar_points = sensor_data.get("lidar", [])
        gps_points = sensor_data.get("gps", [])

        obstacle_detected = any(
            frame.get("risk") == "obstacle" for frame in camera_frames
        ) or any(point.get("obstacle") is True for point in lidar_points)

        return {
            "status": "active",
            "frame_count": len(camera_frames),
            "obstacle_detected": obstacle_detected,
            "gps_points": len(gps_points),
            "lidar_points": len(lidar_points),
            "summary": "Camera, GPS, and LiDAR data fused successfully.",
        }
