from __future__ import annotations

from typing import Any, Dict, List


class SensorStream:
    """Tracks a continuous sensor stream such as camera, GPS, or IMU."""

    def __init__(self, sensor_name: str) -> None:
        self.sensor_name = sensor_name
        self._samples: List[Dict[str, Any]] = []

    def capture(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self._samples.append(payload)
        return {"sensor": self.sensor_name, "payload": payload}

    def snapshot(self) -> Dict[str, Any]:
        alerts = sum(1 for sample in self._samples if sample.get("risk") == "obstacle")
        return {
            "sensor": self.sensor_name,
            "count": len(self._samples),
            "alerts": alerts,
            "samples": list(self._samples),
        }
