from __future__ import annotations

from typing import Any, Dict, List


class TopicController:
    """Minimal ROS2-like topic controller abstraction."""

    def __init__(self, vehicle: str = "drone") -> None:
        self.vehicle = (vehicle or "drone").lower()
        self.topics: Dict[str, List[str]] = {
            "mission": [],
            "telemetry": [],
            "status": [],
        }

    def publish(self, topic: str, payload: Any) -> Dict[str, Any]:
        self.topics.setdefault(topic, [])
        self.topics[topic].append(str(payload))
        return {
            "status": "ok",
            "vehicle": self.vehicle,
            "topic": topic,
            "payload": payload,
        }

    def publish_batch(self, topic: str, payloads: List[Any]) -> Dict[str, Any]:
        for payload in payloads:
            self.publish(topic, payload)
        return {
            "status": "ok",
            "vehicle": self.vehicle,
            "topic": topic,
            "payloads": list(payloads),
        }
