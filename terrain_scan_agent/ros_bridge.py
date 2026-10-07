from __future__ import annotations

from typing import Any, Dict, List


class ROSBridge:
    """Simple ROS2-like bridge translating commands for a vehicle."""

    def __init__(self, vehicle: str = "drone") -> None:
        self.vehicle = (vehicle or "drone").lower()
        self.last_publish: List[str] = []

    def dispatch(self, commands: List[str]) -> Dict[str, Any]:
        self.last_publish = list(commands)
        return {
            "status": "ok",
            "vehicle": self.vehicle,
            "published": list(commands),
        }
