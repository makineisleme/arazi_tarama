from __future__ import annotations

from typing import Any, Dict, List


class LidarCapture:
    """Captures 2D LiDAR range samples and flags nearby obstacles."""

    def __init__(self, sensor_name: str, obstacle_threshold_m: float = 1.5) -> None:
        self.sensor_name = sensor_name
        self.obstacle_threshold_m = obstacle_threshold_m
        self._scans: List[Dict[str, Any]] = []

    def capture_scan(self, samples: List[Dict[str, Any]]) -> Dict[str, Any]:
        obstacle_count = 0
        normalized_samples: List[Dict[str, Any]] = []

        for sample in samples:
            distance = float(sample.get("distance_m", 999.0))
            is_obstacle = distance <= self.obstacle_threshold_m
            if is_obstacle:
                obstacle_count += 1
            normalized_samples.append({
                "angle_deg": sample.get("angle_deg", 0),
                "distance_m": distance,
                "obstacle": is_obstacle,
            })

        payload = {
            "sensor": self.sensor_name,
            "sample_count": len(normalized_samples),
            "obstacle_count": obstacle_count,
            "samples": normalized_samples,
        }
        self._scans.append(payload)
        return payload

    def scan_count(self) -> int:
        return len(self._scans)

    def state(self) -> Dict[str, Any]:
        total_obstacles = sum(scan["obstacle_count"] for scan in self._scans)
        return {
            "sensor": self.sensor_name,
            "scan_count": len(self._scans),
            "obstacles_detected": total_obstacles,
        }
