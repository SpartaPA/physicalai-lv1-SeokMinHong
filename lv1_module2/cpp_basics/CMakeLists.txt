cmake_minimum_required(VERSION 3.10)
project(cpp_basics)

set(CMAKE_CXX_STANDARD 17)

add_executable(stop_distance stop_distance.cpp)

add_executable(cpp_basics
    main.cpp
    motor.cpp
)

add_executable(sensors_demo sensors/main.cpp)
target_include_directories(sensors_demo PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/sensors)

add_executable(sensors_asan sensors/main.cpp)
target_include_directories(sensors_asan PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/sensors)
target_compile_options(sensors_asan PRIVATE -g -fsanitize=address)
target_link_options(sensors_asan PRIVATE -fsanitize=address)