from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Tuple


class LiveCameraCapture:
    """Capture frames from a real camera if available, otherwise produce synthetic frames.

    This keeps the project usable in headless CI environments while still exposing a
    realistic camera interface for real hardware integration later.
    """

    def __init__(self, sensor_name: str, source: int | str = 0, fallback: bool = True) -> None:
        self.sensor_name = sensor_name
        self.source = source
        self.fallback = fallback
        self._frames: List[Dict[str, Any]] = []
        self._camera: Optional[Any] = None
        self._next_id = 1

        self._maybe_open_camera()

    def _maybe_open_camera(self) -> None:
        try:
            import cv2  # type: ignore
        except Exception:
            self._camera = None
            return

        try:
            source = str(self.source)
            if source.isdigit():
                source = int(source)
            self._camera = cv2.VideoCapture(source)
            if not self._camera.isOpened():
                self._camera.release()
                self._camera = None
        except Exception:
            self._camera = None

    def capture_frame(self) -> Dict[str, Any]:
        frame = self._capture_frame_payload()
        self._frames.append(frame)
        return frame

    def capture(self) -> Dict[str, Any]:
        return self.capture_frame()

    def _capture_frame_payload(self) -> Dict[str, Any]:
        frame_id = self._next_id
        self._next_id += 1

        if self._camera is not None:
            try:
                ok, frame = self._camera.read()
                if ok and frame is not None:
                    height, width = frame.shape[:2]
                    payload = {
                        "sensor": self.sensor_name,
                        "source": self.source,
                        "frame_id": frame_id,
                        "timestamp": time.time(),
                        "shape": (height, width, 3),
                        "risk": "normal",
                        "status": "ok",
                        "frame": frame,
                    }
                    return payload
            except Exception:
                pass

        if self.fallback:
            payload = {
                "sensor": self.sensor_name,
                "source": self.source,
                "frame_id": frame_id,
                "timestamp": time.time(),
                "shape": (480, 640, 3),
                "risk": "normal",
                "status": "fallback",
                "frame": None,
            }
            return payload

        raise RuntimeError("Live camera capture is unavailable and fallback is disabled.")

    def frame_count(self) -> int:
        return len(self._frames)

    def state(self) -> Dict[str, Any]:
        risk_count = sum(1 for frame in self._frames if frame.get("risk") == "obstacle")
        return {
            "sensor": self.sensor_name,
            "source": self.source,
            "frame_count": len(self._frames),
            "risk_count": risk_count,
        }

    def close(self) -> None:
        if self._camera is not None:
            self._camera.release()
            self._camera = None
