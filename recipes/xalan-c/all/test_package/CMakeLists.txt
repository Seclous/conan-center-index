cmake_minimum_required(VERSION 3.8)
project(PackageTest CXX)

find_package(XalanC REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example PRIVATE XalanC::XalanC)
target_compile_features(example PRIVATE cxx_std_17)
