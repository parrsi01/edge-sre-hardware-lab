cmake_minimum_required(VERSION 3.20)
project(edge_device_simulator LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(device-simulator src/main.cpp)
target_compile_options(device-simulator PRIVATE -Wall -Wextra -Wpedantic -Werror)

