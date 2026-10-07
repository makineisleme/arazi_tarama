from __future__ import annotations

from typing import Any, Dict, List


class MAVLinkAdapter:
    """A simple MAVLink-style command generator for drone missions."""

    def __init__(self, vehicle: str = "drone") -> None:
        self.vehicle = (vehicle or "drone").lower()
        self.sent: List[str] = []

    def send(self, command: str) -> Dict[str, Any]:
        self.sent.append(command)
        return {
            "status": "ok",
            "vehicle": self.vehicle,
            "command": command,
            "protocol": "mavlink",
        }

    def dispatch(self, commands: List[str]) -> Dict[str, Any]:
        for command in commands:
            self.sent.append(command)
        return {
            "status": "ok",
            "vehicle": self.vehicle,
            "published": list(commands),
            "protocol": "mavlink",
        }
