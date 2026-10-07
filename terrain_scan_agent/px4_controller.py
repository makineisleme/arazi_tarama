from __future__ import annotations

from typing import Any, Dict, List, Union


class PX4Controller:
    """A lightweight PX4-safe wrapper around mission commands for drone control."""

    def __init__(self, vehicle: str = "drone") -> None:
        self.vehicle = vehicle
        self._history: List[Dict[str, Any]] = []

    def send_commands(self, commands: List[Union[str, Dict[str, Any]]]) -> Dict[str, Any]:
        safe = True
        sent: List[Dict[str, Any]] = []

        for command in commands:
            if isinstance(command, str):
                name = command.strip()
                value = None
            elif isinstance(command, dict):
                name = str(command.get("command", "")).strip()
                value = command.get("value")
            else:
                raise TypeError("PX4 commands must be strings or dicts with a command field.")

            if not name:
                continue

            if name in {"arm", "takeoff"} and value is None and isinstance(command, dict):
                safe = False

            sent.append({"command": name, "value": value})
            self._history.append({"command": name, "value": value})

        return {
            "status": "ok",
            "vehicle": self.vehicle,
            "sent_count": len(sent),
            "commands": sent,
            "safe": safe,
        }
