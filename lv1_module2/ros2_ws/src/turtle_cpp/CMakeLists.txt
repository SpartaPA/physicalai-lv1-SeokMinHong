cmake_minimum_required(VERSION 3.8)
set(CMAKE_CXX_STANDARD 17)

project(turtle_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(turtlesim REQUIRED)

add_executable(distance_publisher src/distance_publisher.cpp)
add_executable(distance_listener src/distance_listener.cpp)
ament_target_dependencies(distance_publisher rclcpp std_msgs turtlesim)
ament_target_dependencies(distance_listener rclcpp std_msgs)

install(TARGETS
  distance_publisher
  distance_listener
  DESTINATION lib/${PROJECT_NAME})

ament_package()
