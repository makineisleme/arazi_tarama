from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Sensor:
    name: str
    kind: str


class SensorManager:
    """Tracks active sensors for mission execution."""

    def __init__(self) -> None:
        self._sensors: Dict[str, Sensor] = {}

    def register(self, name: str, kind: str) -> Sensor:
        sensor = Sensor(name=name, kind=kind)
        self._sensors[name] = sensor
        return sensor

    def active_names(self) -> List[str]:
        return list(self._sensors.keys())

    def summary(self) -> Dict[str, object]:
        return {
            "count": len(self._sensors),
            "sensors": [
                {"name": sensor.name, "kind": sensor.kind}
                for sensor in self._sensors.values()
            ],
        }
