from __future__ import annotations

from typing import Any, Dict


class GPSIMUDriver:
    """A simple GPS + IMU driver abstraction for field navigation data."""

    def __init__(self, lat: float = 39.0, lon: float = 35.0, altitude_m: float = 4.0) -> None:
        self.lat = lat
        self.lon = lon
        self.altitude_m = altitude_m

    def read(self) -> Dict[str, Any]:
        return {
            "status": "ok",
            "position": {
                "lat": self.lat,
                "lon": self.lon,
                "altitude_m": self.altitude_m,
            },
            "velocity": {
                "vx_mps": 1.2,
                "vy_mps": 0.4,
                "vz_mps": 0.1,
            },
            "attitude": {
                "roll_deg": 0.3,
                "pitch_deg": 2.1,
                "yaw_deg": 12.5,
            },
            "timestamp": "simulated",
        }
