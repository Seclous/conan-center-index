from conan import ConanFile
from conan.tools.files import copy, get, rm
from conan.tools.layout import basic_layout
import os

required_conan_version = ">=1.52.0"


class LibXsdConan(ConanFile):
    name = "libxsd"
    description = "C++ runtime library for CodeSynthesis XSD (header-only)."
    license = ("GPL-2.0", "FLOSSE")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://codesynthesis.com/projects/xsd/"
    topics = ("xml", "xsd", "headers", "code-synthesis", "schema")

    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    def layout(self):
        basic_layout(self, src_folder="src")

    def package_id(self):
        self.info.clear()

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def package(self):
        # Licenses
        for name in ("LICENSE", "GPLv2", "FLOSSE"):
            copy(self, name, src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"), keep_path=False)

        # Remove files not meant to be packaged
        rm(self, os.path.join("xsd", "buildfile"), self.source_folder)
        rm(self, os.path.join("xsd", "cxx", "version.hxx.in"), self.source_folder)

        # Headers: place xsd folder inside include
        copy(self, pattern="*", src=os.path.join(self.source_folder, "xsd"), dst=os.path.join(self.package_folder, "include", "xsd"))

    def package_info(self):
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []
        # CMake integration
        self.cpp_info.set_property("cmake_file_name", "libxsd")
        self.cpp_info.set_property("cmake_target_name", "libxsd::libxsd")
