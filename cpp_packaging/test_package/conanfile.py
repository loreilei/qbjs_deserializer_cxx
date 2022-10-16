import os
import shutil
import codecs
from conans import ConanFile, CMake, tools


class qbjsDeserializerTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def imports(self):
        self.copy("*.dll", src="bin", dst=os.path.join("install", "bin"))
        self.copy("*.dylib*", src="lib", dst=os.path.join("install", "lib"))
        self.copy("*.so*", src="lib", dst=os.path.join("install", "lib"))
        self.copy("*.lib*", src="lib", dst=os.path.join("install", "lib"))

    def build(self):
        cmake = CMake(self)
        cmake.configure(defs={"CMAKE_INSTALL_PREFIX": "install"})
        cmake.build(target="install")
        shutil.copy(
            src=os.path.join(self.source_folder, "test_data.qbjs"),
            dst=os.path.join("install", "bin"),
        )
        shutil.copy(
            src=os.path.join(self.source_folder, "invalid_qbjs_test_data.qbjs"),
            dst=os.path.join("install", "bin"),
        )

    def test(self):
        testAppPath = os.path.join("install", "bin", "testApp")
        qbjsFilename = os.path.join("install", "bin", "test_data.qbjs")
        outputJsonFilename = os.path.join("install", "bin", "test_data.json")
        invalidHeaderQbjsFilename = os.path.join(
            "install", "bin", "invalid_qbjs_test_data.qbjs"
        )
        outputTextFilename = os.path.join(
            "install", "bin", "invalid_qbjs_test_data_exception_message.txt"
        )

        command = "{0} {1} {2} {3} {4}".format(
            testAppPath,
            qbjsFilename,
            outputJsonFilename,
            invalidHeaderQbjsFilename,
            outputTextFilename,
        )
        self.run(command)

        if os.path.exists(outputJsonFilename):
            with codecs.open(outputJsonFilename, "r", "utf-8") as file:
                data = file.read().rstrip()
                expected_data = '{"baz":"バール","foo":"bar","フー":"bar","食べる":"飲む"}'
                if data == expected_data:
                    # Avoid UTF-8 console printing issues on Windows
                    if tools.os_info.is_windows:
                        print("Succesfully deserialized QBJS file")
                    else:
                        print(
                            "Succesfully deserialized QBJS file (JSON content: "
                            + data
                            + ")"
                        )
                else:
                    raise "Failed to deserialize QBJS file"

            os.remove(outputJsonFilename)
        else:
            raise "Output JSON file expected!"

        if os.path.exists(outputTextFilename):
            with open(outputTextFilename, "r") as file:
                data = file.read().rstrip()
                if data == "Invalid QBJS header tag":
                    print(
                        "Succesfully detected invalid QBJS header (exception message: "
                        + data
                        + ")"
                    )
                else:
                    raise "Failed to detect invalid QBJS header (exception message: " + data + ")"

            os.remove(outputTextFilename)
        else:
            raise "Output text file with exception message expected!"
