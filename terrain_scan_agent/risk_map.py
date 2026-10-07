from __future__ import annotations

from typing import Any, Dict, Iterable, List, Sequence, Tuple


def _risk_to_score(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return max(0.0, min(float(value), 1.0))
    if isinstance(value, str):
        normalized = value.strip().lower()
        mapping = {
            "low": 0.25,
            "medium": 0.55,
            "moderate": 0.55,
            "high": 0.9,
            "critical": 1.0,
            "obstacle": 0.9,
            "anomaly": 0.7,
        }
        return mapping.get(normalized, 0.0)
    return 0.0


def _clamp(value: int, upper: int) -> int:
    return max(0, min(int(value), upper - 1))


def build_risk_map(
    points: Sequence[Dict[str, Any]] | None = None,
    *,
    width: int = 8,
    height: int = 8,
) -> Dict[str, Any]:
    """Create a lightweight risk heatmap from point-like sensor observations.

    Each point may contain x/y coordinates and a risk value. A risk value can be a
    numeric score 0.0-1.0 or a string such as low/medium/high.
    """
    width = max(1, int(width))
    height = max(1, int(height))
    grid = [[0.0 for _ in range(width)] for _ in range(height)]
    hotspots: List[Dict[str, Any]] = []

    if points is None:
        points = []

    for point in points:
        if not isinstance(point, dict):
            continue

        x = point.get("x", point.get("col", point.get("column")))
        y = point.get("y", point.get("row", point.get("line")))
        if x is None and y is None:
            continue

        if x is None:
            x = 0
        if y is None:
            y = 0

        try:
            x_index = _clamp(int(x), width)
            y_index = _clamp(int(y), height)
        except (TypeError, ValueError):
            continue

        risk = _risk_to_score(point.get("risk", point.get("score", point.get("level", 0.0))))
        cell = max(grid[y_index][x_index], risk)
        grid[y_index][x_index] = cell

        hotspots.append({
            "x": x_index,
            "y": y_index,
            "risk": round(cell, 3),
            "label": point.get("label", point.get("type", "risk")),
        })

    if hotspots:
        hotspots.sort(key=lambda item: item["risk"], reverse=True)

    total = sum(cell for row in grid for cell in row)
    max_risk = max((cell for row in grid for cell in row), default=0.0)
    if max_risk >= 0.8:
        summary = "Yüksek riskli bölgeler tespit edildi."
    elif max_risk >= 0.4:
        summary = "Orta düzey risk bulunuyor."
    else:
        summary = "Risk seviyesi düşük veya boş alan." if total == 0 else "Düşük riskli bölgeler gözlemlendi."

    return {
        "status": "ok",
        "width": width,
        "height": height,
        "grid": grid,
        "hotspots": hotspots,
        "risk_score": round(total / max(width * height, 1), 3),
        "max_risk": round(max_risk, 3),
        "summary": summary,
    }


def generate_risk_map(points: Sequence[Dict[str, Any]] | None = None, *, width: int = 8, height: int = 8) -> Dict[str, Any]:
    return build_risk_map(points, width=width, height=height)


def render_risk_map(map_data: Dict[str, Any]) -> str:
    """Render a small ASCII risk map for terminal or log output."""
    grid = map_data.get("grid") or []
    if not grid:
        return "Risk Map\nNo data available."

    rows = ["Risk Map"]
    header = "   " + " ".join(str(col).rjust(2) for col in range(len(grid[0])))
    rows.append(header)

    for row_index, row in enumerate(grid):
        values = " ".join(_cell_to_marker(value) for value in row)
        rows.append(f"{row_index:>2} {values}")

    rows.append(f"Summary: {map_data.get('summary', 'No summary')}")
    return "\n".join(rows)


def _cell_to_marker(value: float) -> str:
    if value >= 0.8:
        return "H"
    if value >= 0.55:
        return "M"
    if value >= 0.25:
        return "L"
    return "."


def build_risk_report(points: Sequence[Dict[str, Any]] | None = None, *, width: int = 8, height: int = 8) -> Dict[str, Any]:
    return build_risk_map(points, width=width, height=height)
