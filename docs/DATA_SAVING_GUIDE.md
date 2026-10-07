# Data Saving Guide

## Current persistence behavior

Running `python main.py` builds an example mission report and writes:

```text
artifacts/
  mission_report.json
  mission_summary.txt
```

The JSON report contains mission status, vehicle, plan action names, commands, selected runtime status, perception summary, fusion output, and risk-map summary metrics. The text summary contains the mission status, vehicle, risk level/score, summary, and commands. Use `terrain_scan_agent.reporting.save_report` and `save_report_text` to select another output directory or filename.

The current report does **not** archive raw camera frames, full GPS/IMU history, or complete LiDAR streams. The dashboard's `/api/status` endpoint serves the supplied in-memory payload plus current camera status; it is not a database or persistent telemetry store.

## Risk map data

`terrain_scan_agent.risk_map` accepts point-like observations with `x`/`y` grid coordinates and a risk score/label. It returns a numeric grid and hotspot list. It does not currently transform GPS latitude/longitude into a georeferenced map.

## Suggested future storage layout

```text
output/
  missions/
    2026-10-07/
      mission_report.json
  telemetry/
    camera/
    gps/
    imu/
    lidar/
```

## Data handling recommendations

- Use UTC timestamps and stable mission identifiers when extending the report schema.
- Keep raw frames in a separate, access-restricted store; avoid placing large binary frames in JSON.
- Avoid persisting camera URL credentials, access tokens, or unnecessary personal/location data.
- Define retention, backup, access-control, and deletion policies before field use.
- Treat simulated/fallback data as synthetic and mark it distinctly from device measurements.

## Future options

SQLite, CSV/Parquet exports, or object storage can be added for historical telemetry; none is currently implemented as a persistent backend.
