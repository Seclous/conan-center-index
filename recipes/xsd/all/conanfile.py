import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.files import (
    apply_conandata_patches, chdir, copy, export_conandata_patches,
    get, rmdir
)

from conan.tools.gnu import Autotools, AutotoolsDeps, AutotoolsToolchain
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

    def export_sources(self):
        export_conandata_patches(self)

    def layout(self):
        basic_layout(self, src_folder="src")

        # Only require Xerces when we build from source (Linux/FreeBSD).

    def requirements(self):
        if str(self.settings.os) in ["Linux", "FreeBSD"]:
            self.requires("xerces-c/[>=3.2.3 <4]")

    def package_id(self):
        del self.info.settings.compiler

    def validate(self):
        os_setting = str(self.settings.os)
        if os_setting not in ["Linux", "FreeBSD", "Windows", "Macos"]:
            raise ConanInvalidConfiguration(
                f"The xsd recipe currently supports Linux, FreeBSD, Windows, and macOS. Got: {os_setting}"
            )
        # Only relevant when we build from source (Linux/FreeBSD)
        if os_setting in ["Linux", "FreeBSD", "Macos"] and self.settings.compiler.cppstd:
            check_min_cppstd(self, 11)

    def source(self):
        pass

    def generate(self):
        # Only needed when building from source
        if str(self.settings.os) in ["Linux", "FreeBSD", "Macos"]:
            tc = AutotoolsToolchain(self)
            tc.extra_cxxflags = ["-std=c++11"]
            tc.extra_ldflags = ["-pthread"]
            tc.generate()
            deps = AutotoolsDeps(self)
            deps.generate()

    def build(self):
        os_key = str(self.settings.os)
        data = self.conan_data["sources"][self.version]

        if os_key in ["Linux", "FreeBSD", "Macos"]:
            # Build from source tarball
            src_entry = data["source"]
            get(self, **src_entry, destination=self.build_folder, strip_root=True)
            apply_conandata_patches(self)
            with chdir(self, self.build_folder):
                autotools = Autotools(self)
                autotools.make()
        else:
            # Windows: fetch prebuilt binary archive
            bin_entry = data[os_key]  # platform-specific URL/checksum
            get(self, **bin_entry, destination=self.build_folder, strip_root=True)
            # No build step needed

    def package(self):
        os_key = str(self.settings.os)

        # Licenses: upstream ships multiple files under xsd/
        copy(self, "LICENSE",
             dst=os.path.join(self.package_folder, "licenses"),
             src=os.path.join(self.source_folder, "xsd"))
        copy(self, "GPLv2",
             dst=os.path.join(self.package_folder, "licenses"),
             src=os.path.join(self.source_folder, "xsd"))
        copy(self, "FLOSSE",
             dst=os.path.join(self.package_folder, "licenses"),
             src=os.path.join(self.source_folder, "xsd"))

        if os_key in ["Linux", "FreeBSD", "Macos"]:
            # Install from the built tree
            with chdir(self, self.source_folder):
                autotools = Autotools(self)
                autotools.install(args=[f"install_prefix={self.package_folder}"])

            # Remove doc/share if unwanted
            rmdir(self, os.path.join(self.package_folder, "share"))

        elif os_key == "Windows":
            copy(self, "bin/*", src=self.build_folder, dst=os.path.join(self.package_folder, "bin"), keep_path=False)


    def package_info(self):
        self.cpp_info.frameworkdirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.resdirs = []
        self.cpp_info.includedirs = []
