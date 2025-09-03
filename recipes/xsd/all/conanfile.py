import os
from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get, copy, rmdir, rm
from conan.tools.layout import basic_layout

required_conan_version = ">=1.52.0"


class ConanXqilla(ConanFile):
    name = "xsd"
    description = (
        "XSD is a W3C XML Schema to C++ translator. "
        "It generates vocabulary-specific, statically-typed C++ mappings (also called bindings) from XML Schema definitions. "
        "XSD supports two C++ mappings: in-memory C++/Tree and event-driven C++/Parser."
    )
    license = ("GPL-2.0", "FLOSSE")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://codesynthesis.com/projects/xsd/"
    topics = ("xml", "xsd", "codegen", "c++")

    package_type = "application"
    settings = "os", "arch", "compiler", "build_type"

    def layout(self):
        basic_layout(self, src_folder="src")

    def package_id(self):
        del self.info.settings.compiler

    def validate(self):
        os_ = str(self.settings.os)
        arch = str(self.settings.arch)
        if os_ not in ["Linux", "Macos", "Windows"]:
            raise ConanInvalidConfiguration(f"Unsupported OS: {os_}")

        # Match your current conandata binaries:
        if os_ == "Linux" and arch != "x86_64":
            raise ConanInvalidConfiguration("This recipe ships Linux x86_64 (glibc 2.31) binaries only.")
        if os_ == "Windows" and arch != "x86_64":
            raise ConanInvalidConfiguration("This recipe ships Windows x86_64 binaries only.")
        if os_ == "Macos" and arch not in ["armv8"]:  # Apple Silicon (aarch64)
            raise ConanInvalidConfiguration("This recipe ships macOS arm64 (aarch64) binaries only.")

    def source(self):
        pass

    def build(self):
        data = self.conan_data["sources"][self.version]
        os_key = str(self.settings.os)
        entry = data[os_key]  # URLs provided per-OS in conandata.yml
        get(self, **entry, destination=self.build_folder, strip_root=True)

    def package(self):
        # Licenses: try common locations/names in the extracted tree
        for name in ("LICENSE*", "GPLv2*", "FLOSSE*"):
            copy(self, f"**/{name}",
                 src=self.build_folder,
                 dst=os.path.join(self.package_folder, "licenses"),
                 keep_path=False)

        # Binaries (handle various archive layouts like bin/, build-release/bin/, root)
        pkg_bin = os.path.join(self.package_folder, "bin")

        copy(self, "**/bin/xsd", src=self.build_folder, dst=pkg_bin, keep_path=False)
        copy(self, "bin/xsd.exe", src=self.build_folder, dst=pkg_bin, keep_path=False)

    def package_info(self):
        self.cpp_info.frameworkdirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.resdirs = []
        self.cpp_info.includedirs = []
