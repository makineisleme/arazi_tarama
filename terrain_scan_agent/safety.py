from __future__ import annotations

from typing import Dict, Any


class SafetyManager:
    """Safety gate for drone and robot operations."""

    def __init__(self, vehicle: str = "drone") -> None:
        self.vehicle = (vehicle or "drone").lower()

    def check(self, altitude_m: float, clearance_m: float) -> Dict[str, Any]:
        max_altitude = 30.0 if self.vehicle == "drone" else 5.0
        min_clearance = 2.0 if self.vehicle == "drone" else 1.0

        if altitude_m > max_altitude:
            return {
                "safe": False,
                "reason": f"Altitude exceeds safe limit for {self.vehicle}: {altitude_m}m > {max_altitude}m.",
            }

        if clearance_m < min_clearance:
            return {
                "safe": False,
                "reason": f"Clearance is below safe minimum for {self.vehicle}: {clearance_m}m < {min_clearance}m.",
            }

        return {
            "safe": True,
            "reason": "Mission is within safe operating limits.",
        }
