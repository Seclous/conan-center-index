cmake_minimum_required(VERSION 3.15)
project(test_package)

# Conan v2: use CMakeDeps/CMakeToolchain; no conanbuildinfo.cmake
find_package(gst-plugins-base CONFIG REQUIRED)
find_package(gstreamer CONFIG REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
# Link against the imported targets provided by the packages
# gstreamer provides gst/gst.h and core functions
target_link_libraries(${PROJECT_NAME} PRIVATE
    gstreamer::gstreamer-1.0
    gst-plugins-base::gstreamer-plugins-base-1.0
)
