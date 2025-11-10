# Known issues
IMU on Realsense does not work with RPi
See: https://github.com/IntelRealSense/librealsense/issues/13108 

ros2 run <pkg> <>.py (needs .py extension)

does not support conda env

to change git to use ssh for authentication:
under <repository>/.git/config
url should have this format
url=ssh://git@github.com/yangjimmy/realsense-ros.git

instead of 
url = https://github.com/yangjimmy/realsense-ros.git
