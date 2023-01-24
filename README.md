## About this crate

This crate exposes the [qbjs_deserializer crate](https://gitlab.com/qbjs_deserializer/qbjs_deserializer) through a C++-style FFI.

__I recommend using Qt6's [QBinaryJson](https://doc.qt.io/qt-6/qbinaryjson.html) on production code__ rather than this crate as it is closer to the original implementation and provided by Qt.

## Build with Conan

1. Clone this repository and move into the root repository
```
git clone https://gitlab.com/qbjs_deserializer/qbjs_deserializer_cxx
cd qbjs_deserializer_cxx
git checkout v0.0.5
```

2. Build the conan package
```
conan create cpp_packaging/conanfile.py qbjs_deserializer/0.0.5-0@<user>/<channel>
```

## Example usage

In your project CMake configuration, find the CMake package
```
find_package(qbjs_deserializer 0.0.5 REQUIRED)
```

If you use conan in your project, you can reference this package in your recipe requirements.

If you don't use conan in your project, you might have to add the conan package installation folder to the CMAKE_PREFIX_PATH variable:
```
cmake -DCMAKE_PREFIX_PATH="path to your qbjs_deserializer/0.0.5-0 conan package root" ...
```

Then link towards the library
```
add_executable(my_project main.cpp) // Add any other relevant file

target_link_libraries(my_project
    PRIVATE
        QBJS_DESERIALIZER::qbjs_deserializer
)
```

Once your cmake project is configured

```cpp
#include <qbjs_deserializer/qbjs_deserializer.hpp>

// In your code...
// 1. Use your favorite API to read the content of the file you want
// to deserialize and get it as a vector of uint8_t
std::vector<uint8_t> fileBinaryContent = // ...

// qbjs_deserializer_cxx transforms qbjs_deserializer's errors into std::exception with a message
try {
    std::string deserialized_qbjs; // Resulting std::string needs to be created on C++ side.
    qbjs_deserializer::deserialize_to_json(fileBinaryContent, deserialized_qbjs);

    // 2. Give this string to your favorite JSON parsing API.

    // 3. Work on your data...
}
catch (std::exception& e) {
    // In this example, simply print to the standard error channel the exception message
    std::cerr << e.what() << std::endl;
}
```

## Error messages in exception

qbjs_deserializer_cxx checks qbjs_deserializer errors and returns an exception with a matching error message. Here is the correspondance table:

| qbjs_deserializer error | qbjs_deserializer_cxx exception message |
| - | - |
| [qbjs::DeserializeError::InsufficientData](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/qbjs/enum.DeserializeError.html#variant.InsufficientData) | Not enough data to analyze (slice too small) |
| [qbjs::DeserializeError::InvalidRootContainer](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/qbjs/enum.DeserializeError.html#variant.InvalidRootContainer) | Root value isn't an object or an array (invalid root container) |
| [qbjs::analysis::header::Error::InvalidLength](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/analysis/header/enum.Error.html#variant.InvalidLength) | Invalid QBJS header length |
| [qbjs::analysis::header::Error::InvalidTag](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/analysis/header/enum.Error.html#variant.InvalidTag) | Invalid QBJS header tag |
| [qbjs::analysis::header::Error::InvalidVersion](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/analysis/header/enum.Error.html#variant.InvalidVersion) | Invalid QBJS header version |
| [qbjs::analysis::metadata::Error::InvalidContainerBaseLength](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/analysis/metadata/enum.Error.html#variant.InvalidContainerBaseLength) | Attempted to read an array or an object but reached end of slice |
| [qbjs::analysis::metadata::Error::InvalidValueHeaderSize](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/analysis/metadata/enum.Error.html#variant.InvalidValueHeaderSize) | Attempted to read a value header but reached end of slice |
| [qbjs::analysis::data::Error::UnknownQtValue](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/analysis/data/enum.Error.html#variant.UnknownQtValue) | Unknown Qt value (doesn't match QJsonValue::ValueType enum) |
| [qbjs::analysis::data::Error::InvalidValueLength](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/analysis/data/enum.Error.html#variant.InvalidValueLength) | Attempted to read some data but reached end of slice |
| [qbjs::analysis::data::Error::InvalidArrayContainer](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/analysis/data/enum.Error.html#variant.InvalidArrayContainer) | Attempted to read an array (indicated by value header) but container has the object flag set |
| [qbjs::analysis::data::Error::InvalidObjectContainer](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/analysis/data/enum.Error.html#variant.InvalidObjectContainer) | Attempted to read an object (indicated by value header) but container doesn't have the object flag set |
| [qbjs::read::ReadError::FailedToDecodeLatin1String](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/read/enum.ReadError.html#variant.FailedToDecodeLatin1String) | Failed to decode Latin 1 string (key or value) |
| [qbjs::read::ReadError::FailedToDecodeUtf16String](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/read/enum.ReadError.html#variant.FailedToDecodeUtf16String) | Failed to decode UTF-16 string (key or value) |
| [qbjs::read::ReadError::InvalidBoolDataPosition](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/read/enum.ReadError.html#variant.InvalidBoolDataPosition) | Attempted to read a bool value but reached end of slice |
| [qbjs::read::ReadError::InvalidSelfContainedNumberDataPosition](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/read/enum.ReadError.html#variant.InvalidSelfContainedNumberDataPosition) | Attempted to read a (self-container) number value but reached end of slice |
| [qbjs::read::ReadError::InvalidNumberDataRange](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/read/enum.ReadError.html#variant.InvalidNumberDataRange) | Attempted to read a number value but reached end of slice |
| [qbjs::read::ReadError::InvalidLatin1StringDataRange](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/read/enum.ReadError.html#variant.InvalidLatin1StringDataRange) | Attempted to read a Latin 1 string (key or value) but reached end of slice |
| [qbjs::read::ReadError::InvalidUtf16StringDataRange](https://docs.rs/qbjs_deserializer/0.0.5/qbjs_deserializer/read/enum.ReadError.html#variant.InvalidUtf16StringDataRange) | Attempted to read a UTF-16 string (key or value) but reached end of slice |

## Conan packaging and CMake finder testing
To test the C++ packaging with conan and the CMake finders, [Gitlab CI pipelines](https://gitlab.com/qbjs_deserializer/qbjs_deserializer_cxx/-/pipelines) is set up to create the conan package on Linux, Windows, and MacOS (3 different jobs).

The conan package also use the C++ bindings in the test apps, trying to deserialize a simple JSON object with Latin1 and Utf16 string encodings in keys and values. [More complete testing of the deserialization of QBJS files is done in the integration tests of the Rust crate](https://gitlab.com/qbjs_deserializer/qbjs_deserializer/-/blob/main/tests/validation_tests.rs).