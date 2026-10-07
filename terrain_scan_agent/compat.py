from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class VehicleAdapter:
    name: str
    commands: List[str] = field(default_factory=list)

    def send(self, command: str) -> str:
        self.commands.append(command)
        return f"{self.name}: {command}"


class DroneAdapter(VehicleAdapter):
    def __init__(self):
        super().__init__(name="drone")


class RobotAdapter(VehicleAdapter):
    def __init__(self):
        super().__init__(name="robot")
