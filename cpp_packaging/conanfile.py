from conans import ConanFile, CMake, tools
import os
import configparser
from subprocess import check_call
import glob


class qbjsDeserializerConan(ConanFile):
    name = "qbjs_deserializer"
    lib_version = "0.0.2"
    recipe_version = "0"
    version = "{}-{}".format(lib_version, recipe_version)
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {}
    default_options = {}
    url_base = "https://github.com/loreilei/qbjs_deserializer_cxx"
    url = "{}.git".format(url_base)
    exports = []
    description = (
        "qbjs_desrializer_cxx is C++ style FFI for the qbjs_deserializer Rust crate."
    )
    license = "{0}/blob/{1}/LICENSE.txt".format(url_base, lib_version)

    def export_sources(self):
        self.copy("*")
        self.copy("*", src="../rust", dst="{}/rust".format(self.export_sources_folder), keep_path=True)

    def build(self):
        rust_brige_crate_root = "rust"
        self.run("cd {} && cargo build --release".format(rust_brige_crate_root))

        qbjs_deserializer_cxx_bridge_src_path = (
            "{}/target/cxxbridge/qbjs_deserializer_cxx/src/".format(
                rust_brige_crate_root
            )
        )

        qbjs_deserializer_root = "qbjs_deserializer"

        tools.mkdir(qbjs_deserializer_root)
        tools.mkdir("{}/include/qbjs_deserializer".format(qbjs_deserializer_root))
        tools.mkdir("{}/src".format(qbjs_deserializer_root))
        tools.mkdir("{}/lib".format(qbjs_deserializer_root))

        tools.rename(
            "{}/qbjs_deserializer.rs.cc".format(qbjs_deserializer_cxx_bridge_src_path),
            "{}/src/qbjs_deserializer.cpp".format(qbjs_deserializer_root),
        )
        tools.rename(
            "{}/qbjs_deserializer.rs.h".format(qbjs_deserializer_cxx_bridge_src_path),
            "{}/include/qbjs_deserializer/qbjs_deserializer.hpp".format(
                qbjs_deserializer_root
            ),
        )

        qbjs_deserializer_target_release_path = "{}/target/release/".format(rust_brige_crate_root)
        tools.rename(
            "{}/libqbjs_deserializer_cxx.a".format(qbjs_deserializer_target_release_path),
            "{}/lib/libqbjs_deserializer_cxx.a".format(qbjs_deserializer_root),
        )

        # Use glob to find libcxxbridge1.a because the output folder starting with cxx- has a hash and can't be hardcoded
        for libcxxbridge1 in glob.glob(
            "{}/build/cxx-*/out/libcxxbridge1.a".format(qbjs_deserializer_target_release_path)
        ):
            tools.rename(
                libcxxbridge1, "{}/lib/libcxxbridge1.a".format(qbjs_deserializer_root)
            )

        cmake = CMake(self, parallel=True)
        cmake.configure(source_dir="../", build_dir="build")
        cmake.build(target="install")

    def package(self):
        self.copy("LICENSE.txt", ".", ".", keep_path=False)
        self.copy(
            "qbjs_deserializer/include/qbjs_deserializer/qbjs_deserializer.hpp",
            src=".",
            dst="include/qbjs_deserializer/",
            keep_path=False,
        )
        self.copy("build/libqbjs_deserializer.so", src=".", dst="lib/", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.libs = [
            "qbjs_deserializer",
        ]
