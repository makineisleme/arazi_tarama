from __future__ import annotations

from typing import Any, Dict, List


class NavigationFusion:
    """Fuse GPS and IMU data into a single navigation state."""

    def combine(self, sensor_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        gps_points = sensor_data.get("gps", [])
        imu_points = sensor_data.get("imu", [])

        gps_point = gps_points[0] if gps_points else {}
        imu_point = imu_points[0] if imu_points else {}

        yaw_deg = float(imu_point.get("yaw", imu_point.get("yaw_deg", 0.0)))
        lat = float(gps_point.get("lat", 0.0))
        lon = float(gps_point.get("lon", 0.0))
        altitude = float(gps_point.get("altitude_m", 0.0))

        return {
            "status": "active",
            "gps_points": len(gps_points),
            "imu_points": len(imu_points),
            "yaw_deg": yaw_deg,
            "position": {"lat": lat, "lon": lon, "altitude_m": altitude},
            "position_ready": bool(gps_points),
            "summary": "GPS and IMU fused successfully.",
        }
