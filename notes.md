# Known issues
IMU on Realsense does not work with RPi
See: https://github.com/IntelRealSense/librealsense/issues/13108 

To get rbg and depth images only,
ros2 launch realsense2_camera rs_launch.py enable_color:=true enable_depth:=true

ros2 run <pkg> <>.py (needs .py extension)

does not support conda env

to change git to use ssh for authentication:
under <repository>/.git/config
url should have this format
url=ssh://git@github.com/yangjimmy/realsense-ros.git

instead of 
url = https://github.com/yangjimmy/realsense-ros.git

convert between ros img and opencv image: use cv bridge
sudo apt-get install ros-(ROS version name)-cv-bridge


