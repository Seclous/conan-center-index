cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

find_package(HDiffPatch CONFIG REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example HDiffPatch::hdiffpatch)
