from __future__ import annotations

from typing import Dict, Any, List


class DroneAdapter:
    """MAVLink-style command abstraction for drone missions."""

    def __init__(self, vehicle: str = "drone") -> None:
        self.vehicle = (vehicle or "drone").lower()
        self.history: List[str] = []

    def send(self, command: str) -> Dict[str, Any]:
        self.history.append(command)
        return {
            "status": "ok",
            "vehicle": self.vehicle,
            "command": command,
            "protocol": "mavlink",
        }
