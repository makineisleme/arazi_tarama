# Architecture

## Overview

This project implements a layered prototype for terrain scanning using a drone/robot, camera, GPS, IMU, and LiDAR-inspired inputs. The system is designed to convert user intent into a safe, executable mission and then provide telemetry, analysis, and reporting.

## Main layers

### 1. Planning layer
- `terrain_scan_agent/planner.py`
- Converts natural-language requests into action steps.
- Produces structured mission actions such as scan, capture, analyze, report.

### 2. Mission and safety layer
- `terrain_scan_agent/mission.py`
- `terrain_scan_agent/safety.py`
- Builds mission context and validates altitude, margin, and operational safety limits.
- Prevents unsafe missions from reaching execution.

### 3. Control layer
- `terrain_scan_agent/control.py`
- `terrain_scan_agent/px4_controller.py`
- Converts mission commands into executable control actions for a drone or robot.

### 4. Sensor and acquisition layer
- `terrain_scan_agent/sensors.py`
- `terrain_scan_agent/live_camera.py`
- `terrain_scan_agent/real_camera.py`
- `terrain_scan_agent/lidar_capture.py`
- `terrain_scan_agent/gps_imu_driver.py`
- `terrain_scan_agent/navigation_fusion.py`
- Manages device registration, frame capture, GPS/IMU readouts, LiDAR scans, and fused navigation state.

### 5. Perception and analytics layer
- `terrain_scan_agent/vision.py`
- `terrain_scan_agent/sensor_fusion.py`
- `terrain_scan_agent/processor.py`
- Computes risk, obstacles, and aggregated telemetry summaries.

### 6. Integration and transport layer
- `terrain_scan_agent/ros_bridge.py`
- `terrain_scan_agent/mavlink_adapter.py`
- `terrain_scan_agent/ros_mavlink_bridge.py`
- `terrain_scan_agent/topic_controller.py`
- Bridges logical actions into ROS-style or MAVLink-like command flows.

### 7. Runtime and presentation layer
- `terrain_scan_agent/field_runtime.py`
- `terrain_scan_agent/dashboard.py`
- `terrain_scan_agent/ui.py`
- Orchestrates the full demo run and generates user-facing summary data.

## Runtime flow

1. User prompt enters the planner.
2. Mission is created and safety-checked.
3. Control commands are generated.
4. Camera, GPS, IMU, and LiDAR data are acquired.
5. Telemetry is fused and processed.
6. Risks are identified.
7. Report and dashboard output are generated.

## Safety principles

- altitude limits are enforced
- minimum safety margin is required
- mission execution stops when the operation is unsafe
- camera fallback logic prevents crash in headless environments

## Extension points

- replace simulated drivers with real hardware adapters
- add database persistence for telemetry
- add REST API or websocket dashboard
- add real PX4 or ROS2 integration
- add map generation and georeferenced risk layers

## Project entrypoint

- `main.py` executes the full sample workflow.
- `run.sh` loads the local virtual environment and runs the application.
- `setup.sh` installs dependencies and initializes the project environment.
