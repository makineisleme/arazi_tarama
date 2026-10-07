# CLAUDE Project Guide

## Purpose

This repository contains a terrain scanning prototype for drones/robots. It is designed to support planning, mission generation, safety validation, sensing, telemetry fusion, and reporting.

## Commands

### Setup
```bash
cd /workspaces/arazi_tarama
./setup.sh
```

### Run demo
```bash
cd /workspaces/arazi_tarama
./run.sh
```

### Run tests
```bash
cd /workspaces/arazi_tarama
. .venv/bin/activate
python -m pytest -q
```

### Run the live dashboard
```bash
cd /workspaces/arazi_tarama
. .venv/bin/activate
terrain-scan-dashboard --camera /dev/video0
```

## Important project conventions

- Keep logic modular and hardware-agnostic.
- Prefer simulation-safe default behavior when real devices are unavailable.
- Validate safety before mission execution.
- Keep sensor interfaces consistent across modules.
- For new features, add a failing test first.

## Repo structure

- `terrain_scan_agent/` – main Python implementation
- `tests/` – regression tests
- `main.py` – end-to-end demo entrypoint
- `README.md` – public overview
- `progress.md` – project status log

## Safe workflow

1. Understand the prompt.
2. Plan actions and commands.
3. Evaluate safety.
4. Execute only if mission is safe.
5. Capture telemetry.
6. Analyze risk and generate report.

## When adding modules

- Put new logic inside `terrain_scan_agent/`.
- Export public API in `terrain_scan_agent/__init__.py`.
- Add tests under `tests/`.
- Prefer deterministic behavior for CI compatibility.

## Notes for AI agents

- Do not assume real hardware is available.
- Use synthetic or fallback behavior when headless or offline.
- The dashboard has no built-in authentication or TLS; keep it on localhost or behind appropriate access controls.
- Distinguish fallback frames and simulated sensor values from real device measurements.
- Keep interfaces minimal and testable.
- Favor compatibility with a drone/robot controller abstraction rather than a single vendor integration.
