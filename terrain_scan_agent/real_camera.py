from __future__ import annotations

import time
from typing import Any, Dict, Optional


class RealCameraReader:
    """Read real camera frames when OpenCV is present, otherwise fall back to synthetic data."""

    def __init__(self, sensor_name: str = "front_cam", source: int = 0) -> None:
        self.sensor_name = sensor_name
        self.source = source
        self._camera: Optional[Any] = None
        self._frame_id = 1

        self._connect()

    def _connect(self) -> None:
        try:
            import cv2  # type: ignore
        except Exception:
            self._camera = None
            return

        try:
            self._camera = cv2.VideoCapture(self.source)
        except Exception:
            self._camera = None

    def read_frame(self) -> Dict[str, Any]:
        payload = {
            "sensor": self.sensor_name,
            "source": self.source,
            "frame_id": self._frame_id,
            "timestamp": time.time(),
            "status": "fallback",
            "risk": "normal",
            "shape": (480, 640, 3),
            "frame": None,
        }
        self._frame_id += 1

        if self._camera is None:
            return payload

        try:
            import cv2  # type: ignore

            ok, frame = self._camera.read()
            if ok and frame is not None:
                height, width = frame.shape[:2]
                payload["status"] = "ok"
                payload["shape"] = (height, width, 3)
                payload["frame"] = frame
                return payload
        except Exception:
            pass

        return payload

    def close(self) -> None:
        if self._camera is not None:
            try:
                self._camera.release()
            except Exception:
                pass
            self._camera = None
