from __future__ import annotations

from typing import Any, Dict, Optional

from .control import Controller
from .gps_imu_driver import GPSIMUDriver
from .live_camera import LiveCameraCapture
from .mission import create_mission
from .navigation_fusion import NavigationFusion
from .px4_controller import PX4Controller
from .real_camera import RealCameraReader


class FieldRuntime:
    """Unify live camera, navigation, and flight control into one scan runtime."""

    def __init__(
        self,
        vehicle: str = "drone",
        camera_name: str = "front_cam",
        camera_source: Any = 0,
        gps_source: Optional[str] = None,
        gps_mode: str = "simulated",
    ) -> None:
        self.vehicle = (vehicle or "drone").lower()
        self.camera_name = camera_name
        self.camera = LiveCameraCapture(camera_name, source=camera_source, fallback=True)
        self.camera_reader = RealCameraReader(sensor_name=camera_name, source=camera_source)
        self.gps_driver = GPSIMUDriver(
            lat=39.0,
            lon=35.0,
            altitude_m=3.0,
            source=gps_source,
            mode=gps_mode,
        )
        self.navigation = NavigationFusion()
        self.controller = Controller(vehicle=self.vehicle)
        self.px4 = PX4Controller(vehicle=self.vehicle)

    def run_scan(
        self,
        prompt: str,
        altitude_m: float = 3.0,
        safety_margin_m: float = 5.0,
    ) -> Dict[str, Any]:
        mission = create_mission(
            prompt,
            vehicle=self.vehicle,
            altitude_m=altitude_m,
            safety_margin_m=safety_margin_m,
        )

        if mission["status"] != "safe":
            return {
                "status": "unsafe",
                "vehicle": self.vehicle,
                "camera": {"sensor": self.camera_name},
                "navigation": {"position_ready": False},
                "report": {"summary": "Mission aborted before field execution."},
                "mission": mission,
            }

        camera_frame = self.camera.capture_frame()
        gps_state = self.gps_driver.read()
        navigation = self.navigation.combine({
            "gps": [{"lat": gps_state["position"]["lat"], "lon": gps_state["position"]["lon"], "altitude_m": gps_state["position"]["altitude_m"]}],
            "imu": [{"roll": 0.0, "pitch": 0.2, "yaw": gps_state["attitude"]["yaw_deg"]}],
        })
        control_result = self.controller.execute(mission["commands"])
        flight_result = self.px4.send_commands([
            {"command": "arm", "value": True},
            {"command": "takeoff", "value": float(altitude_m)},
        ])

        report = {
            "summary": (
                f"Live {self.vehicle} scan completed with {camera_frame['frame_id']} camera capture "
                f"and {navigation['gps_points']} GPS point(s)."
            ),
            "camera_frame": camera_frame["frame_id"],
            "flight_status": flight_result["status"],
            "controller_status": control_result["status"],
            "safety": mission["safety"]["status"],
        }

        return {
            "status": mission["status"],
            "vehicle": self.vehicle,
            "camera": {
                "sensor": camera_frame["sensor"],
                "source": camera_frame["source"],
                "frame_id": camera_frame["frame_id"],
                "risk": camera_frame.get("risk", "normal"),
            },
            "gps": gps_state,
            "navigation": navigation,
            "controller": control_result,
            "flight": flight_result,
            "report": report,
            "mission": mission,
        }
