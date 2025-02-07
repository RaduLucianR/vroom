cmake_minimum_required(VERSION 3.8)
project(vroom_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(vroom_interf REQUIRED)

add_library(vroomWPi SHARED
	src/vroomWPi.c
)
target_link_libraries(vroomWPi PUBLIC wiringPi)

add_executable(talker src/publisher.cpp)
ament_target_dependencies(talker rclcpp std_msgs)

add_executable(listener src/subscriber.cpp)
ament_target_dependencies(listener rclcpp std_msgs)

add_executable(wheelEnabler src/wheelEnabler.cpp)
ament_target_dependencies(wheelEnabler rclcpp std_msgs)
target_link_libraries(wheelEnabler vroomWPi)
set_target_properties(wheelEnabler PROPERTIES
	INSTALL_RPATH "$ORIGIN"
)

add_executable(xboxInput src/xboxInput.cpp)
ament_target_dependencies(xboxInput rclcpp std_msgs vroom_interf)
target_link_libraries(xboxInput evdev)

add_executable(gas src/gas.cpp)
ament_target_dependencies(gas rclcpp std_msgs)
target_link_libraries(gas vroomWPi)
set_target_properties(gas PROPERTIES
	INSTALL_RPATH "$ORIGIN"
)

add_executable(controller src/controller.cpp)
ament_target_dependencies(controller rclcpp std_msgs vroom_interf)

add_executable(wire src/testWiringPi.cpp)
ament_target_dependencies(wire rclcpp)
target_link_libraries(wire vroomWPi)
set_target_properties(wire PROPERTIES
	INSTALL_RPATH "$ORIGIN"
)

install(TARGETS
  talker
  listener
  wire
  wheelEnabler
  xboxInput
  vroomWPi
  gas
  controller
  DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()


#ament_export_targets(${PROJECT_NAME}-targets HAS_LIBRARY_TARGET)
ament_package()
