cmake_minimum_required(VERSION 3.10)
project(cpp_basics)

set(CMAKE_CXX_STANDARD 17)

add_executable(stop_distance stop_distance.cpp)

add_executable(cpp_basics
    main.cpp
    motor.cpp
)

add_executable(loop_demo sensors/loop.cpp)
add_executable(heap_stack_demo sensors/heap_stack.cpp)
add_executable(count_demo sensors/count.cpp)

add_executable(leak_demo sensors/leaks.cpp)
target_compile_options(leak_demo PRIVATE -fsanitize=address)
