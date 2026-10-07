from __future__ import annotations

from typing import Dict, Any


class RobotAdapter:
    """Navigation and control abstraction for ground robots."""

    def __init__(self, vehicle: str = "robot") -> None:
        self.vehicle = (vehicle or "robot").lower()
        self.history = []

    def send(self, command: str) -> Dict[str, Any]:
        self.history.append(command)
        return {
            "status": "ok",
            "vehicle": self.vehicle,
            "command": command,
            "protocol": "ros2",
        }
