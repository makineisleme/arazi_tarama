from __future__ import annotations

from typing import Any, Dict, List


def analyze_scan(scan_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simple heuristic perception layer for scanning results."""
    annotations: List[str] = scan_data.get("annotations") or []
    object_count = len(annotations)

    if object_count >= 3:
        risk_level = "high"
        summary = "Yüksek risk: çoklu engel/anomali tespit edildi."
    elif object_count >= 1:
        risk_level = "medium"
        summary = "Orta risk: sınırlı sayıda anomali bulundu."
    else:
        risk_level = "low"
        summary = "Düşük risk: anomali tespit edilmedi."

    return {
        "risk_level": risk_level,
        "detected_objects": object_count,
        "summary": summary,
    }
