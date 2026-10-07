from __future__ import annotations

from typing import Any, Dict, List


class CameraCapture:
    """Stores camera frames and counts risk events."""

    def __init__(self, sensor_name: str) -> None:
        self.sensor_name = sensor_name
        self._frames: List[Dict[str, Any]] = []

    def capture(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self._frames.append(payload)
        return {"sensor": self.sensor_name, "frame": payload}

    def state(self) -> Dict[str, Any]:
        risk_count = sum(1 for frame in self._frames if frame.get("risk") == "obstacle")
        return {
            "sensor": self.sensor_name,
            "frame_count": len(self._frames),
            "risk_count": risk_count,
            "frames": list(self._frames),
        }
