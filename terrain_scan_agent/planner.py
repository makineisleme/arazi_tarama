from __future__ import annotations

from typing import Dict, List


def build_action_plan(task_text: str) -> List[Dict[str, object]]:
    """Create a simple action plan from a user request."""
    task = (task_text or "").lower()
    plan: List[Dict[str, object]] = []

    if "tarama" in task or "scan" in task or "arama" in task:
        plan.append({
            "action": "scan_area",
            "description": "Belirtilen alanı tarama moduyla kontrol et.",
            "priority": 1,
        })

    plan.append({
        "action": "capture_frames",
        "description": "Görüntü ve sensör verilerini yakala.",
        "priority": 2,
    })

    plan.append({
        "action": "analyze_results",
        "description": "Toplanan verileri işle ve riskli alanları tespit et.",
        "priority": 3,
    })

    plan.append({
        "action": "report",
        "description": "Sonuçları kullanıcıya özetle.",
        "priority": 4,
    })

    if not plan:
        plan.append({
            "action": "ask_for_target",
            "description": "Hedef alan ve görev türünü netleştir.",
            "priority": 1,
        })

    return plan


def generate_vehicle_commands(plan: List[Dict[str, object]], vehicle: str = "drone") -> List[str]:
    """Translate a task plan into vehicle command names for compatible systems."""
    vehicle_name = (vehicle or "drone").lower()

    if "robot" in vehicle_name:
        return [
            "start_navigation",
            "move_to_waypoint",
            "scan_environment",
            "collect_sensor_data",
            "return_to_base",
        ]

    return [
        "takeoff",
        "move_to_waypoint",
        "start_scan",
        "capture_frame",
        "return_home",
    ]
