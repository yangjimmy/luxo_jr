# Project Structure

```
src/
├── camera/              # Camera module with hand detection (primary camera work)
│   ├── nodes/          # ROS2 nodes (predict_node.py, listen_node.py)
│   ├── detection/      # YOLO hand detection system
│   └── README.md       # Detailed camera module documentation
├── servo/              # Servo/robotic arm control module
├── interfaces/         # ROS2 message/service definitions
└── realsense-ros/      # RealSense camera driver (for reference)
```

---

# Usage & Configuration

## Running Camera Module (Hand Detection)
The camera module is now organized in `src/camera/` with clean separation of concerns.

**Start RealSense Camera:**
```bash
ros2 launch realsense2_camera rs_launch.py enable_color:=true enable_depth:=true
```

**Run Hand Detection Node:**
```bash
ros2 run camera predict_node
```

For more details, see `src/camera/README.md`

## Running ROS2 Nodes (General)
```bash
ros2 run <package> <node>.py  # Note: requires .py extension
```

Examples:
```bash
ros2 run servo *.py
```

## Environment
- Does not support conda environments
- Use system Python instead

## Git Authentication (SSH Setup)
Edit `<repository>/.git/config` and change the URL format:

**SSH format (recommended):**
```
url = ssh://git@github.com/yangjimmy/realsense-ros.git
```

**HTTPS format (alternative):**
```
url = https://github.com/yangjimmy/realsense-ros.git
```

## OpenCV Integration
- Use `cv-bridge` to convert between ROS images and OpenCV images
- Install: `sudo apt-get install ros-(ROS_VERSION)-cv-bridge`

---

## Building the Workspace

Follow these steps from your workspace root (`/home/jimmy/ros2_ws`) to build packages.

1) Source the ROS 2 distribution (replace `<ros2-distro>` with your distro, e.g. `jazzy`):
```bash
source /opt/ros/jazzy/setup.bash
```

2) Build the entire workspace:
```bash
cd /home/jimmy/ros2_ws
colcon build
```

3) Or build only the `camera` package during development (faster):
```bash
cd /home/jimmy/ros2_ws
colcon build --packages-select camera
```

4) After a successful build, source the workspace install to use the newly built packages:
```bash
source /home/jimmy/ros2_ws/install/setup.bash
```

Notes:
- It's fine that you removed any `build/` or `install/` directories under `src/` — `colcon build` expects `build/`, `install/`, and `log/` at the workspace root and will recreate them there.
- If dependencies are missing, install them via `apt` for system ROS packages or `pip` for Python-only dependencies, then rebuild.
- If `ros2 run camera predict_node` reports "No executable found", make sure you sourced `install/setup.bash` in the same shell after building.


# RealSense Launch Commands

## RGB and Depth Images Only
```bash
ros2 launch realsense2_camera rs_launch.py enable_color:=true enable_depth:=true
```

## RGB and Depth Images with Alignment
```bash
ros2 launch realsense2_camera rs_launch.py enable_color:=true enable_depth:=true align_depth.enable:=true
```

---

# Known Issues

## RealSense IMU
- IMU on RealSense does not work with Raspberry Pi
- See: https://github.com/IntelRealSense/librealsense/issues/13108 

## NumPy Compatibility
- cv-bridge is not compatible with NumPy 2.x; only supports NumPy 1.x
- cv-bridge should already be installed with ROS2 Jazzy
