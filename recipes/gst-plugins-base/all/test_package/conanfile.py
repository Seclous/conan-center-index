from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.build import can_run
import os


class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeToolchain", "CMakeDeps", "VirtualRunEnv"

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        # Require the package being created under test
        self.requires(self.tested_reference_str)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if can_run(self):
            bin_dir = self.cpp.build.bindirs[0] if self.cpp.build.bindirs else os.path.join(self.build_folder, "bin")
            exe = "test_package.exe" if self.settings.os == "Windows" else "test_package"
            bin_path = os.path.join(bin_dir, exe)
            self.run(bin_path, env="conanrun")
