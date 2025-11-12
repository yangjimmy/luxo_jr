# CMake generated Testfile for 
# Source directory: /home/jimmy/ros2_ws/src/realsense-ros/realsense2_camera
# Build directory: /home/jimmy/ros2_ws/build/realsense2_camera
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(gtest_template "/home/jimmy/.venv/bin/python3" "-u" "/opt/ros/jazzy/share/ament_cmake_test/cmake/run_test.py" "/home/jimmy/ros2_ws/build/realsense2_camera/test_results/realsense2_camera/gtest_template.gtest.xml" "--package-name" "realsense2_camera" "--output-file" "/home/jimmy/ros2_ws/build/realsense2_camera/ament_cmake_gtest/gtest_template.txt" "--command" "/home/jimmy/ros2_ws/build/realsense2_camera/gtest_template" "--gtest_output=xml:/home/jimmy/ros2_ws/build/realsense2_camera/test_results/realsense2_camera/gtest_template.gtest.xml")
set_tests_properties(gtest_template PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/jimmy/ros2_ws/build/realsense2_camera/gtest_template" TIMEOUT "60" WORKING_DIRECTORY "/home/jimmy/ros2_ws/build/realsense2_camera" _BACKTRACE_TRIPLES "/opt/ros/jazzy/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/jazzy/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;95;ament_add_test;/opt/ros/jazzy/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/jimmy/ros2_ws/src/realsense-ros/realsense2_camera/CMakeLists.txt;384;ament_add_gtest;/home/jimmy/ros2_ws/src/realsense-ros/realsense2_camera/CMakeLists.txt;0;")
subdirs("gtest")
