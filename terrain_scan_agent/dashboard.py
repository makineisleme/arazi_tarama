from __future__ import annotations

import html
import json
from typing import Any, Dict, List


def _safe_text(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, default=str)
    return str(value)


def _metric_rows(report: Dict[str, Any]) -> str:
    rows: List[str] = []
    for key, value in report.items():
        if key in {"status", "vehicle", "summary", "commands"}:
            continue
        rows.append(
            f"<tr><th>{html.escape(str(key))}</th>"
            f"<td>{html.escape(_safe_text(value))}</td></tr>"
        )

    commands = report.get("commands") or []
    if commands:
        rendered_commands = "<ul>" + "".join(
            f"<li>{html.escape(_safe_text(item))}</li>" for item in commands
        ) + "</ul>"
        rows.append(f"<tr><th>commands</th><td>{rendered_commands}</td></tr>")

    return "\n".join(rows) if rows else "<tr><td colspan='2'>No additional metrics</td></tr>"


def build_dashboard_html(report: Dict[str, Any]) -> str:
    """Render the live camera dashboard and its initial mission summary."""
    status = html.escape(str(report.get("status", "unknown")).lower())
    vehicle = html.escape(str(report.get("vehicle", "drone")))
    summary = html.escape(str(report.get("summary", "Mission ready.")))
    rows_html = _metric_rows(report)
    badge_color = "#16a34a" if status in {"ok", "safe", "active"} else "#f59e0b"

    return f"""<!doctype html>
<html lang="tr">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Arazi Tarama Dashboard</title>
    <style>
      :root {{ color-scheme: dark; font-family: system-ui, sans-serif; }}
      body {{ margin: 0; padding: 1.25rem; background: #0f172a; color: #e2e8f0; }}
      main {{ max-width: 1200px; margin: auto; }}
      h1 {{ margin-top: 0; }}
      .layout {{ display: grid; grid-template-columns: minmax(0, 2fr) minmax(280px, 1fr); gap: 1rem; }}
      .card {{ background: #111827; border: 1px solid #334155; border-radius: 12px; padding: 1rem; min-width: 0; }}
      .badge {{ display: inline-block; padding: .3rem .7rem; border-radius: 999px; background: {badge_color}; color: white; font-weight: 700; }}
      .video {{ display: block; width: 100%; min-height: 240px; max-height: 70vh; object-fit: contain; background: #020617; border-radius: 8px; }}
      .muted {{ color: #94a3b8; }}
      table {{ width: 100%; border-collapse: collapse; margin-top: .75rem; overflow-wrap: anywhere; }}
      th, td {{ border-bottom: 1px solid #334155; padding: .6rem; text-align: left; vertical-align: top; }}
      th {{ width: 34%; color: #cbd5e1; }}
      pre {{ white-space: pre-wrap; overflow-wrap: anywhere; }}
      @media (max-width: 760px) {{ body {{ padding: .75rem; }} .layout {{ grid-template-columns: 1fr; }} }}
    </style>
  </head>
  <body>
    <main>
      <h1>Arazi Tarama Dashboard</h1>
      <div class="layout">
        <section class="card">
          <h2>Canlı kamera</h2>
          <img class="video" src="/stream.mjpg" alt="Canlı kamera akışı" />
          <p id="camera-state" class="muted">Kamera bağlantısı bekleniyor…</p>
        </section>
        <section class="card" aria-live="polite">
          <h2>Misyon durumu</h2>
          <p><strong>Araç:</strong> <span id="vehicle">{vehicle}</span></p>
          <p><strong>Durum:</strong> <span id="status" class="badge">{status}</span></p>
          <p id="summary">{summary}</p>
          <h3>Canlı durum verisi</h3>
          <pre id="live-data">Durum yükleniyor…</pre>
        </section>
      </div>
      <section class="card" style="margin-top: 1rem">
        <h2>Görev ayrıntıları</h2>
        <table><tbody>{rows_html}</tbody></table>
      </section>
    </main>
    <script>
      async function refreshStatus() {{
        try {{
          const response = await fetch('/api/status', {{ cache: 'no-store' }});
          if (!response.ok) throw new Error(`HTTP ${{response.status}}`);
          const data = await response.json();
          document.getElementById('vehicle').textContent = data.vehicle ?? 'unknown';
          document.getElementById('status').textContent = data.status ?? 'unknown';
          document.getElementById('summary').textContent = data.summary ?? '';
          document.getElementById('live-data').textContent = JSON.stringify(data, null, 2);
          const camera = data.camera ?? {{}};
          document.getElementById('camera-state').textContent =
            `Kamera: ${{camera.status ?? 'bekleniyor'}} · Kare: ${{camera.frame_id ?? 0}} · Kaynak: ${{camera.source ?? '-'}}`;
        }} catch (error) {{
          document.getElementById('camera-state').textContent = `Durum alınamadı: ${{error}}`;
        }}
      }}
      refreshStatus();
      setInterval(refreshStatus, 2000);
    </script>
  </body>
</html>
"""
