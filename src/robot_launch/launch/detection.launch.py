from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Get RealSense package share directory
    realsense_share = get_package_share_directory('realsense2_camera')
    realsense_launch = os.path.join(realsense_share, 'launch', 'rs_launch.py')

    # RealSense camera launch file
    camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(realsense_launch),
        launch_arguments={
            'enable_color': 'true',
            'enable_depth': 'true',
        }.items(),
    )

    # Detection node (show all output on console)
    detection_node = Node(
        package='detection',
        executable='predict_node',
        name='predict_node',
        output='screen',
        emulate_tty=True,
    )

    return LaunchDescription([
        camera_launch,
        detection_node,
    ])
