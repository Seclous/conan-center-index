import os
from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain, CMakeDeps
from conan.tools.files import copy, apply_conandata_patches, get


class HDiffPatchConan(ConanFile):
    name = "hdiffpatch"
    version = "5.0.1"
    license = "MIT"
    url = "https://github.com/sisong/HDiffPatch"
    description = "Binary and directory differential compression (patch) tools."
    topics = ("diff", "patch", "compression", "zstd", "lzma", "zlib")
    settings = "os", "compiler", "build_type", "arch"
    package_type = "library"

    # Options mirrored from the main CMakeLists.txt
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "enable_dir_diff": [True, False],
        "enable_multithread": [True, False],
        "enable_vcdiff": [True, False],
        "enable_bsdiff": [True, False],
        "enable_md5": [True, False],
        "enable_xxhash": [True, False],
        "enable_bzip2": [True, False],
        "enable_libdeflate": [True, False],
        "enable_zlib": [True, False],
        "enable_lzma": [True, False],
        "enable_zstd": [True, False],
        "build_tools": [True, False],
        "build_tests": [True, False],
    }

    default_options = {
        "shared": False,
        "fPIC": True,
        "enable_dir_diff": True,
        "enable_multithread": True,
        "enable_vcdiff": True,
        "enable_bsdiff": True,
        "enable_md5": True,
        "enable_xxhash": True,
        "enable_bzip2": True,
        "enable_libdeflate": True,
        "enable_zlib": True,
        "enable_lzma": True,
        "enable_zstd": True,
        "build_tools": True,
        "build_tests": False,
    }

    exports_sources = "patches/*"

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        apply_conandata_patches(self)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["HDIFFPATCH_BUILD_TOOLS"] = self.options.build_tools
        tc.variables["HDIFFPATCH_BUILD_TESTS"] = self.options.build_tests
        tc.variables["HDIFFPATCH_ENABLE_DIR_DIFF"] = self.options.enable_dir_diff
        tc.variables["HDIFFPATCH_ENABLE_MULTITHREAD"] = self.options.enable_multithread
        tc.variables["HDIFFPATCH_ENABLE_VCDIFF"] = self.options.enable_vcdiff
        tc.variables["HDIFFPATCH_ENABLE_BSDIFF"] = self.options.enable_bsdiff
        tc.variables["HDIFFPATCH_ENABLE_MD5"] = self.options.enable_md5
        tc.variables["HDIFFPATCH_ENABLE_XXHASH"] = self.options.enable_xxhash
        tc.variables["HDIFFPATCH_ENABLE_ZLIB"] = self.options.enable_zlib
        tc.variables["HDIFFPATCH_ENABLE_LIBDEFLATE"] = self.options.enable_libdeflate
        tc.variables["HDIFFPATCH_ENABLE_BZIP2"] = self.options.enable_bzip2
        tc.variables["HDIFFPATCH_ENABLE_LZMA"] = self.options.enable_lzma
        tc.variables["HDIFFPATCH_ENABLE_ZSTD"] = self.options.enable_zstd

        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

        if self.options.build_tests:
            self.run("ctest", cwd=self.build_folder)

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "HDiffPatch")
        self.cpp_info.set_property("cmake_target_name", "HDiffPatch::hdiffpatch")
        self.cpp_info.libs = ["hdiffpatch"]

        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs.append("pthread")
