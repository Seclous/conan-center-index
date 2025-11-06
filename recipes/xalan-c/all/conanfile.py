import os

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMakeDeps, CMake, cmake_layout, CMakeToolchain
from conan.tools.scm import Git
from conan.tools.files import apply_conandata_patches, copy, get, rmdir

class XalanCConan(ConanFile):
    name = "xalan-c"
    version= "1.12.0"
    license = "Apache 2.0"
    author = "David N Bertoni, Scott Boag, Shane Curcuru, Jack Donohue, Paul Dick, Emily Farmer, Donald Leslie, David Marston, Myriam Midy, Robert Weir"
    url = "https://github.com/apache/xalan-c"
    description = "The Apache Xalan-C++ Project provides a library and a command line program to transform XML documents using a stylesheet that conforms to XSLT 1.0 standards."
    settings = "os", "compiler", "build_type", "arch"
    
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": False,
    }
    
    package_type = "library"
    exports_sources = "patches/*"

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        apply_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        self.options["xerces-c"].shared = self.options.shared
        # This library requires C++17
        self.settings.compiler.cppstd = "17"

    def validate(self):
        """Ensure that the compiler supports at least C++17."""
        required_cppstd = "17"

    def requirements(self):
        self.requires("xerces-c/[>=3.3.0 <3.4.0]", transitive_headers = True)  # XML parser
        self.requires("icu/74.2", transitive_headers = True)  # Unicode support

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.cache_variables["XALANC_BUILD_EXAMPLES"] = False
        tc.cache_variables["XALANC_BUILD_TESTS"] = False
        tc.cache_variables["XALANC_BUILD_DOCS"] = False
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "XalanC")
        self.cpp_info.set_property("cmake_target_name", "XalanC::XalanC")
        self.cpp_info.set_property("pkg_config_name", "XalanC")

        version_tokens = self.version.split(".")

        if self.settings.os == "Windows":
            xalan_lib = "Xalan-C_%s" % version_tokens[0]
            xalan_msg_lib = "XalanMsgLib_%s" % version_tokens[0]

            if self.settings.build_type == "Debug":
                xalan_lib += "D"
                xalan_msg_lib += "D"
        else:
            xalan_lib = "xalan-c"
            xalan_msg_lib = "xalanMsg"

        self.cpp_info.libs = [xalan_lib,xalan_msg_lib]
        self.cpp_info.requires = ["xerces-c::xerces-c", "icu::icu"]
