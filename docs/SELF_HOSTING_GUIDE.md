# Self Hosting Guide

## Goal

This guide describes how to run the terrain scanning project on a private server or self-managed infrastructure without depending on a hosted SaaS layer.

## Requirements

- Linux server or VM
- Python 3.10+
- Git
- optional: camera hardware, GPS/IMU, PX4 bridge or ROS2 stack
- optional: reverse proxy or SSL certificate

## Deployment layout

```text
/opt/arazi-tarama/
  app/
  venv/
  logs/
  data/
```

## Installation

```bash
git clone <repo-url>
cd arazi_tarama
./setup.sh
```

## Service pattern

Use a systemd service or a simple process manager for long-running deployment. Example:

```bash
cd /workspaces/arazi_tarama
PYTHONPATH=/workspaces/arazi_tarama python main.py
```

## Recommended production hardening

- run as a dedicated non-root user
- keep environment variables in a dedicated config file
- log mission data to a structured directory
- limit access to raw sensor output and reports
- use TLS and authenticated endpoints for external access

## Data retention

Use a dedicated directory for persisted scan outputs, reports, and machine logs.

## Operational checklist

- validate startup script
- verify sensors and drivers
- test safety logic before every mission
- check disk space and log rotation
- ensure back-ups for mission reports

## Notes

This repository is intentionally designed to be hardware-agnostic and therefore suitable for self-hosted experimentation and controlled field deployment.
