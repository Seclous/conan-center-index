cmake_minimum_required(VERSION 3.15)
project(test_package)

# Conan v2: use CMakeDeps/CMakeToolchain; no conanbuildinfo.cmake
find_package(gst-plugins-base CONFIG REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
# Link against the imported target provided by the package
target_link_libraries(${PROJECT_NAME} PRIVATE gst-plugins-base::gstreamer-plugins-base-1.0)
