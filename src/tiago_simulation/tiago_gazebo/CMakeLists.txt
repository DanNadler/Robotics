cmake_minimum_required(VERSION 3.4.0)
project(tiago_gazebo)

# Find the necessary packages
find_package(ament_cmake_auto REQUIRED)
ament_auto_find_build_dependencies()

# Include message generation
find_package(rosidl_default_generators REQUIRED)

# Include your custom message files
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Order.msg"  # Add your message file(s) here
)

# Install scripts
install(
  PROGRAMS scripts/tuck_arm.py scripts/talker.py scripts/listener.py scripts/head_control.py scripts/vision.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()

  find_package(launch_testing_ament_cmake REQUIRED)
  find_package(play_motion2_msgs REQUIRED)
  find_package(sensor_msgs REQUIRED)

  # tuck_arm_test
  ament_add_gtest_executable(tuck_arm_test
    test/tuck_arm_test.cpp
  )
  ament_target_dependencies(tuck_arm_test
    launch_testing_ament_cmake
    play_motion2_msgs
    rclcpp
    sensor_msgs
  )

  install(
    TARGETS tuck_arm_test
    DESTINATION share/${PROJECT_NAME}/test
  )

  add_launch_test(
    test/tuck_arm_test.launch.py
  )
endif()

ament_auto_package(INSTALL_TO_SHARE launch)
