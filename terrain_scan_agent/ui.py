from __future__ import annotations

from typing import Any, Dict


def render_summary(mission: Dict[str, Any]) -> str:
    lines = [
        "=== Mission Summary ===",
        f"Status: {mission['status']}",
        f"Vehicle: {mission['vehicle']}",
        f"Summary: {mission['summary']}",
        "Commands:",
    ]

    for command in mission.get("commands", []):
        lines.append(f"- {command}")

    return "\n".join(lines)
