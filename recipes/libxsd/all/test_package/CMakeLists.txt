cmake_minimum_required(VERSION 3.15)
project(test_package CXX)

find_package(libxsd REQUIRED)

add_executable(test_package src/test.cpp)
target_link_libraries(test_package PRIVATE libxsd::libxsd)
