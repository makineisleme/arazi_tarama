from __future__ import annotations

from typing import Any, Dict


def build_dashboard_html(report: Dict[str, Any]) -> str:
    """Render a minimal HTML dashboard for mission status and high-level metrics."""
    status = str(report.get("status", "unknown")).lower()
    vehicle = str(report.get("vehicle", "drone"))
    summary = str(report.get("summary", "Mission ready."))

    rows = []
    for key, value in list(report.items()):
        if key in {"status", "vehicle", "summary"}:
            continue
        rows.append(f"<tr><th>{key}</th><td>{value}</td></tr>")

    rows_html = "\n".join(rows) if rows else "<tr><td colspan='2'>No additional metrics</td></tr>"

    return f"""
<!doctype html>
<html lang="tr">
  <head>
    <meta charset="utf-8" />
    <title>Arazi Tarama Dashboard</title>
    <style>
      body {{ font-family: Arial, sans-serif; margin: 2rem; background: #0f172a; color: #e2e8f0; }}
      .card {{ background: #111827; border: 1px solid #334155; border-radius: 12px; padding: 1.2rem; max-width: 900px; }}
      .badge {{ display: inline-block; padding: 0.35rem 0.8rem; border-radius: 999px; background: #16a34a; color: white; font-weight: bold; }}
      table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
      th, td {{ border-bottom: 1px solid #334155; padding: 0.7rem; text-align: left; }}
      td {{ color: #cbd5e1; }}
    </style>
  </head>
  <body>
    <div class="card">
      <h1>Arazi Tarama Dashboard</h1>
      <p><strong>Vehicle:</strong> {vehicle}</p>
      <p><strong>Status:</strong> <span class="badge">{status}</span></p>
      <p><strong>Summary:</strong> {summary}</p>
      <table>
        <tbody>
          {rows_html}
        </tbody>
      </table>
    </div>
  </body>
</html>
"""
