# Changelog

These entries describe prototype milestones, not published package releases. The installable package version is maintained in `pyproject.toml`; see [VERSION.md](VERSION.md).

## Current work

### Added
- x/y-cell risk grid with numeric scores, hotspot list, summary, and ASCII rendering.
- JSON and text mission report exports under `artifacts/`.
- Local dashboard CLI with configurable camera source, host, port, FPS, and optional JSON report input.
- Shared MJPEG `/stream.mjpg` camera endpoint and `/api/status` JSON endpoint.
- Responsive dashboard page with periodic status refresh and escaped user-supplied HTML content.
- Camera fallback stream for headless/no-camera operation and redaction of URL credentials/query values in status responses.
- `terrain-scan-dashboard` package entry point and expanded HTTP/stream tests.

### Changed
- Setup installs the project as an editable package.
- README, architecture, setup, self-hosting, data-saving, and progress documentation now describe the implemented capabilities and hardware limitations.

## Earlier prototype milestones (historically labeled 0.1.0–0.3.0)

### 0.1.0 milestone
- Planner, mission safety checks, basic vehicle commands, sensor registry, perception summary, and demo workflow.

### 0.2.0 milestone
- LiDAR and sensor fusion support.

### 0.3.0 milestone
- LiDAR capture, sensor fusion, navigation fusion, adapters for ROS/MAVLink/PX4-style interfaces, and field runtime.
- Real camera reader, GPS/IMU driver abstraction, HTML dashboard rendering, and regression tests.
