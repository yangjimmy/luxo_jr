# robot_launch

Central launch package for the robot system. Contains all launch configurations for running the robot with different settings and modes.

## Quick Start

Launch the default detection pipeline (RealSense camera + hand detection):

```bash
ros2 launch robot_launch detection.launch.py
```

## Available Launch Files

- **`detection.launch.py`** — Starts RealSense camera 

## Creating New Launch Files

### Structure

Each launch file should be placed in the `launch/` directory with a `.py` extension and follow the ROS2 launch file convention.

### Minimal Template

Create a new file `launch/my_demo.launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Example: Include another launch file
    # some_package_share = get_package_share_directory('some_package')
    # some_launch = os.path.join(some_package_share, 'launch', 'some_launch.py')
    # some_launch_include = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(some_launch),
    #     launch_arguments={'arg1': 'value1'}.items(),
    # )

    # Example: Launch a ROS2 node
    # my_node = Node(
    #     package='my_package',
    #     executable='my_executable',
    #     name='my_node_name',
    #     output='screen',
    #     emulate_tty=True,
    # )

    return LaunchDescription([
        # Add your nodes and includes here
    ])
```

### Best Practices

1. **Use `get_package_share_directory()`** to locate resources from other ROS packages. This ensures portability across different installations.
   ```python
   from ament_index_python.packages import get_package_share_directory
   pkg_share = get_package_share_directory('your_package_name')
   ```

2. **Use `os.path.join()`** to build paths reliably across operating systems.
   ```python
   config_file = os.path.join(pkg_share, 'config', 'params.yaml')
   ```

3. **Set `output='screen'`** during development to see node logs directly in the terminal. Remove or set to `'log'` for production.
   ```python
   Node(
       package='detection',
       executable='predict_node',
       output='screen',
       emulate_tty=True,  # Allows colors in output
   )
   ```

4. **Include other launch files** to reuse configurations and reduce duplication.
   ```python
   IncludeLaunchDescription(
       PythonLaunchDescriptionSource(path_to_launch),
       launch_arguments={'param': 'value'}.items(),
   )
   ```

5. **Document parameters** and node names clearly in comments so others understand what each launch file does.

### Example: Multi-Mode Launch File

Here's an example that launches detection with optional arguments:

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Declare launch arguments
    enable_camera = DeclareLaunchArgument(
        'enable_camera',
        default_value='true',
        description='Enable RealSense camera'
    )
    enable_detection = DeclareLaunchArgument(
        'enable_detection',
        default_value='true',
        description='Enable hand detection node'
    )

    # Use launch arguments
    camera_enabled = LaunchConfiguration('enable_camera')
    detection_enabled = LaunchConfiguration('enable_detection')

    # Conditionally include camera
    realsense_share = get_package_share_directory('realsense2_camera')
    realsense_launch = os.path.join(realsense_share, 'launch', 'rs_launch.py')

    camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(realsense_launch),
        launch_arguments={
            'enable_color': 'true',
            'enable_depth': 'true',
        }.items(),
        condition=IfCondition(camera_enabled),
    )

    # Detection node
    detection_node = Node(
        package='detection',
        executable='predict_node',
        output='screen',
        emulate_tty=True,
        condition=IfCondition(detection_enabled),
    )

    return LaunchDescription([
        enable_camera,
        enable_detection,
        camera_launch,
        detection_node,
    ])
```

Run with custom arguments:
```bash
ros2 launch robot_launch my_demo.launch.py enable_camera:=false
```

## Testing a New Launch File

After creating a new launch file, test it:

```bash
# Rebuild the workspace
colcon build --packages-select robot_launch

# Source the workspace
source install/setup.bash

# Run your launch file
ros2 launch robot_launch my_new_launch.launch.py
```

## Troubleshooting

### "No launch file found" Error
- Make sure your `.py` file is in the `launch/` directory.
- Rebuild with `colcon build --packages-select robot_launch`.
- Source the workspace again: `source install/setup.bash`.

### "Package not found" Error
- Verify the package name is correct in `get_package_share_directory()`.
- Ensure the package is built and installed: `colcon build --packages-select <package_name>`.

### Node fails to start
- Check that the executable name exists in the target package: `ros2 run <package> <executable>`.
- Verify all required dependencies are built and sourced.
- Check node output with `ros2 topic echo` or `ros2 node info` for diagnostics.

## References

- [ROS2 Launch Documentation](https://docs.ros.org/en/jazzy/Concepts/Intermediate/Launch/Launch-system.html)
- [Launch File Syntax](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html)
