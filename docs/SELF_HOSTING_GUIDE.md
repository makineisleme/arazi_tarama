# Self-Hosting Guide

## Goal and current scope

This guide covers running the prototype and its local camera dashboard on self-managed infrastructure. It is not a production flight-control deployment recipe.

## Requirements

- Linux server or VM
- Python 3.10+
- Git
- Optional: USB/RTSP camera, GPS/IMU hardware, and separately validated PX4/ROS2 integration
- For remote access: a secured reverse proxy with TLS and authentication

## Installation

```bash
git clone <repo-url>
cd arazi_tarama
./setup.sh
. .venv/bin/activate
```

## Run the dashboard

The server binds to localhost by default:

```bash
terrain-scan-dashboard --camera /dev/video0 --report artifacts/mission_report.json
```

For an RTSP camera:

```bash
terrain-scan-dashboard --camera 'rtsp://user:password@camera-host/stream'
```

The dashboard is served at `/`, the MJPEG stream at `/stream.mjpg`, and the status JSON at `/api/status`. When the camera is unavailable, fallback mode publishes a synthetic placeholder; use `--no-camera-fallback` to fail the stream instead.

Do not expose the built-in HTTP server directly to an untrusted network. It has no authentication or TLS. If remote access is needed, bind it only on a trusted interface and place it behind a correctly configured authenticated TLS reverse proxy/firewall. Camera URL credentials and query parameters are redacted from the status payload, but should still be managed as secrets.

## Service operation

Use a service manager only after testing startup, shutdown, camera permissions, report paths, and log handling in the target environment. Keep the service under a dedicated unprivileged account and restrict access to camera devices and generated reports.

## Operational limitations

- The dashboard and test suite do not validate physical camera performance or flight safety.
- GPS/IMU and PX4/MAVLink integrations require real drivers, configuration, and independent field validation.
- Preserve a manual override and independent safety procedures for any real vehicle.
- Keep reports, raw sensor output, and camera URLs out of public logs.
