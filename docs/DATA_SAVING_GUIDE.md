# Data Saving Guide

## Goal

This project can capture and process scan data, telemetry, and mission metadata. The repository is intentionally modular so that data can later be persisted to local disk, remote storage, or a database.

## Current data types

### Mission metadata
- prompt
- vehicle type
- flight or robot mission status
- commands generated
- safety summary

### Sensor data
- camera frames
- GPS points
- IMU values
- LiDAR scan samples

### Analysis outputs
- risk level
- obstacle count
- telemetry summaries
- sensor fusion report

## Recommended storage pattern

Use a structured folder layout like:

```text
output/
  missions/
    2026-10-07/
      mission.json
  telemetry/
    camera/
    GPS/
    imu/
    lidar/
  reports/
    summary.json
    dashboard.html
```

## Suggested schema

```json
{
  "mission_id": "2026-10-07-001",
  "vehicle": "drone",
  "prompt": "Bu arazide tarama yap",
  "status": "safe",
  "altitude_m": 4.0,
  "safety_margin_m": 5.0,
  "commands": ["takeoff", "move_to_waypoint", "start_scan"],
  "risk_level": "high",
  "timestamp": "2026-10-07T12:00:00Z"
}
```

## Save flow

1. mission is created
2. control commands are generated
3. sensor data is captured
4. per-frame events are logged
5. final summary is exported to JSON or HTML

## Best practices

- save raw payloads beside processed summaries
- use UTC timestamps
- compress large frame archives if necessary
- avoid writing secrets or tokens into local logs
- keep schema backward-compatible when evolving the project

## Future upgrade path

- local SQLite database
- parquet or CSV exports for analysis
- object storage (S3, MinIO)
- web dashboard with live history
