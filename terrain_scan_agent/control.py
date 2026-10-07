from __future__ import annotations

from typing import Dict, List


class Controller:
    """Abstracts the execution layer for drone/robot commands."""

    def __init__(self, vehicle: str = "drone") -> None:
        self.vehicle = (vehicle or "drone").lower()
        self.command_log: List[str] = []

    def execute(self, commands: List[str]) -> Dict[str, object]:
        self.command_log = list(commands)
        return {
            "status": "ok",
            "vehicle": self.vehicle,
            "executed": list(commands),
        }
