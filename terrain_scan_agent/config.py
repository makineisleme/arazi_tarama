"""Configuration defaults for the terrain scan prototype."""

DEFAULT_SENSORS = {
    "camera": True,
    "imu": True,
    "gps": True,
    "lidar": False,
    "depth_camera": False,
}

SUPPORTED_VEHICLES = {"drone", "robot"}
