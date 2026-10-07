from __future__ import annotations

from typing import Any, Dict, List


class ROSMAVLinkBridge:
    """A lightweight bridge layer for ROS2/MAVLink style vehicle command publishing."""

    def __init__(self, vehicle: str = "drone") -> None:
        self.vehicle = vehicle
        self._published: List[Dict[str, Any]] = []

    def send(self, commands: List[Dict[str, Any]]) -> Dict[str, Any]:
        topics: List[str] = []
        for command in commands:
            topic = command.get("topic")
            message = command.get("message", {})
            self._published.append({"topic": topic, "message": message})
            if topic:
                topics.append(topic)

        return {
            "status": "ok",
            "vehicle": self.vehicle,
            "published_count": len(self._published),
            "topics": topics,
            "payload": list(self._published),
        }
