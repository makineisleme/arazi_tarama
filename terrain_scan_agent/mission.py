from __future__ import annotations

from typing import Any, Dict, List

from .planner import build_action_plan, generate_vehicle_commands


def evaluate_safety(vehicle: str, altitude_m: float, safety_margin_m: float) -> Dict[str, Any]:
    """Return safety metadata for mission validation."""
    vehicle_name = (vehicle or "drone").lower()

    if vehicle_name == "drone":
        max_altitude = 30.0
        min_margin = 2.0
    else:
        max_altitude = 5.0
        min_margin = 1.0

    if altitude_m < 0:
        return {
            "status": "unsafe",
            "reason": "Altitude cannot be negative.",
            "max_altitude_m": max_altitude,
            "safety_margin_m": safety_margin_m,
        }

    if altitude_m > max_altitude:
        return {
            "status": "unsafe",
            "reason": f"Altitude exceeds safe limit for {vehicle_name}.",
            "max_altitude_m": max_altitude,
            "safety_margin_m": safety_margin_m,
        }

    if safety_margin_m < min_margin:
        return {
            "status": "unsafe",
            "reason": "Safety margin is below minimum allowed value.",
            "max_altitude_m": max_altitude,
            "safety_margin_m": safety_margin_m,
        }

    return {
        "status": "safe",
        "reason": "Mission is within safe operating limits.",
        "max_altitude_m": max_altitude,
        "safety_margin_m": safety_margin_m,
    }


def create_mission(
    prompt: str,
    vehicle: str = "drone",
    altitude_m: float = 3.0,
    safety_margin_m: float = 5.0,
) -> Dict[str, Any]:
    """Create a full mission descriptor from a user prompt."""
    plan = build_action_plan(prompt)
    commands = generate_vehicle_commands(plan, vehicle=vehicle)
    safety = evaluate_safety(vehicle, altitude_m, safety_margin_m)

    if safety["status"] != "safe":
        return {
            "status": "unsafe",
            "vehicle": (vehicle or "drone").lower(),
            "altitude_m": altitude_m,
            "safety": safety,
            "plan": plan,
            "commands": [],
            "summary": "Mission aborted due to safety policy.",
        }

    return {
        "status": "safe",
        "vehicle": (vehicle or "drone").lower(),
        "altitude_m": altitude_m,
        "safety": safety,
        "plan": plan,
        "commands": commands,
        "summary": (
            f"{(vehicle or 'drone').lower()} mission prepared with {len(plan)} plan steps "
            f"and {len(commands)} vehicle commands."
        ),
    }
