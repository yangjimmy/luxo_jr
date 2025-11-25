cmake_minimum_required(VERSION 3.8)
project(detection)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)

# Install Python package
ament_python_install_package(detection)

# Install entry point scripts
install(PROGRAMS
  scripts/predict_node.py
  scripts/listen_node.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files
#install(DIRECTORY
#  launch
#  DESTINATION share/${PROJECT_NAME}
#)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
endif()

ament_package()
