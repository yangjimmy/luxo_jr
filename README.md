# Project Structure

```
src/
├── detection/          # Hand detection with YOLO (primary detection work)
│   ├── nodes/         # ROS2 nodes (predict_node.py, listen_node.py)
│   ├── detection/     # YOLO hand detection system
│   └── README.md      # Detailed detection module documentation
├── servo/             # Servo/robotic arm control module
├── interfaces/        # ROS2 message/service definitions
├── robot_launch/      # Central launch files for robot system
├── realsense-ros/     # RealSense camera driver (for reference)
```

---

# Quick Start

## Build the Workspace

From `/home/jimmy/ros2_ws`:

```bash
# Source ROS2 distribution
source /opt/ros/jazzy/setup.bash

# Build all packages (or use --packages-select detection for just the detection module)
colcon build

# Source the workspace install
source install/setup.bash
```

## Run the Detection Pipeline

**Start RealSense Camera + Detection Node** (single command, both run together):
```bash
ros2 launch robot_launch detection.launch.py
```

Alternatively, if you prefer to run them separately:

- **Start RealSense Camera Only:**
```bash
ros2 launch realsense2_camera rs_launch.py enable_color:=true enable_depth:=true
```

- **Run Hand Detection Node** (in a new terminal):
```bash
ros2 run detection predict_node
```

For more details on launch configurations and how to create new launch files, see [src/robot_launch/README.md](src/robot_launch/README.md) and [src/detection/README.md](src/detection/README.md)

---

# Launch Files

All system launch files are centralized in the `robot_launch` package. This approach keeps the workspace organized and makes it easy to add new launch configurations for different scenarios (e.g., different demos, calibration modes, test setups).

## Available Launch Files

- **`detection.launch.py`** — Starts RealSense camera (color + depth) and hand detection node

## Creating New Launch Files

To add a new launch configuration:

1. Create a new `.py` file in `src/robot_launch/launch/` (e.g., `my_demo.launch.py`)
2. Follow the template in [src/robot_launch/README.md](src/robot_launch/README.md#creating-new-launch-files)
3. Rebuild: `colcon build --packages-select robot_launch`
4. Run: `ros2 launch robot_launch my_demo.launch.py`

See the [robot_launch README](src/robot_launch/README.md) for detailed examples and best practices.

---

# Common ROS2 Commands

```bash
# List available packages
ros2 pkg list

# List topics being published
ros2 topic list

# Echo a topic's messages
ros2 topic echo /topic_name

# List running nodes
ros2 node list

# Get info about a package
ros2 pkg prefix detection

# Run a ROS2 node
ros2 run <package> <executable>

# Launch a launch file
ros2 launch <package> <launch_file>

# View ROS2 logs
ros2 run ament_cmake_core ament_cmake_environment_hooks_DIR
```

---

# Building & Development

## Full Rebuild

Clean and rebuild all packages:
```bash
cd /home/jimmy/ros2_ws
rm -rf build install log
colcon build
```

## Build Specific Package

Build only the detection module:
```bash
colcon build --packages-select detection
```

## Environment

- Does not support conda environments
- Use system Python instead

---

# Supplementary Information

## RealSense Camera Options

### RGB and Depth with Alignment
```bash
ros2 launch realsense2_camera rs_launch.py enable_color:=true enable_depth:=true align_depth.enable:=true
```

## OpenCV Integration

- Use `cv-bridge` to convert between ROS images and OpenCV images
- Install: `sudo apt-get install ros-(ROS_VERSION)-cv-bridge`

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

---

# Known Issues

## RealSense IMU
- IMU on RealSense does not work with Raspberry Pi
- See: https://github.com/IntelRealSense/librealsense/issues/13108 

## NumPy Compatibility
- cv-bridge is not compatible with NumPy 2.x; only supports NumPy 1.x
- cv-bridge should already be installed with ROS2 Jazzy

## Build Issues

### "No executable found" Error
If `ros2 run detection predict_node` reports "No executable found":
- Ensure you sourced `install/setup.bash` in the same shell after building
- Try cleaning and rebuilding: `rm -rf build install && colcon build`

### Missing Dependencies
If dependencies are missing during build:
- Install via `apt` for system ROS packages
- Install via `pip` for Python-only dependencies
- Then rebuild with `colcon build`

### Module Import Errors
Verify the detection module structure:
```bash
ls -la src/detection/detection/
ls -la src/detection/detection/configs/
ls -la src/detection/detection/models/
```
