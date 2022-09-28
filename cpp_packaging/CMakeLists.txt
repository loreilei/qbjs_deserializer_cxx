cmake_minimum_required(VERSION 3.23)

project(qbjs_deserializer VERSION 0.0.2)

find_package(Threads REQUIRED)

if (UNIX AND NOT APPLE)
    set(QBJS_DESERIALIZER_PLATFORM_SPECIFIC_LINK_LIBRARIES
        dl
    )
elseif (MSVC)
    set(QBJS_DESERIALIZER_PLATFORM_SPECIFIC_LINK_LIBRARIES
        userenv
        ws2_32
        bcrypt
    )
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

if (MSVC)
    set(LIB_FILE_PREFIX )
    set(LIB_FILE_EXTENSION lib)
else()
    set(LIB_FILE_PREFIX lib)
    set(LIB_FILE_EXTENSION a)
endif()

add_library(qbjs_deserializer SHARED
            ${CMAKE_SOURCE_DIR}/qbjs_deserializer/include/qbjs_deserializer/qbjs_deserializer.hpp
            ${CMAKE_SOURCE_DIR}/qbjs_deserializer/src/qbjs_deserializer.cpp
        )

set_property(TARGET qbjs_deserializer PROPERTY CXX_STANDARD 17)
set_property(TARGET qbjs_deserializer PROPERTY CMAKE_CXX_STANDARD_REQUIRED TRUE)
set_property(TARGET qbjs_deserializer PROPERTY CMAKE_SKIP_RPATH TRUE)

target_link_libraries(qbjs_deserializer
    PUBLIC
    ${QBJS_DESERIALIZER_PLATFORM_SPECIFIC_LINK_LIBRARIES}
    PRIVATE
    Threads::Threads
    ${CMAKE_SOURCE_DIR}/qbjs_deserializer/lib/${LIB_FILE_PREFIX}qbjs_deserializer_cxx.${LIB_FILE_EXTENSION}
    ${CMAKE_SOURCE_DIR}/qbjs_deserializer/lib/${LIB_FILE_PREFIX}cxxbridge1.${LIB_FILE_EXTENSION}
)


install(TARGETS qbjs_deserializer
    EXPORT qbjs_deserializerTargets
    FILE_SET HEADERS
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include)

install(EXPORT qbjs_deserializerTargets
    FILE qbjs_deserializerTargets.cmake
    NAMESPACE QBJS_DESERIALIZER::
    DESTINATION lib/cmake/qbjs_deserializer)

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    "qbjs_deserializerConfigVersion.cmake"
    VERSION ${qbjs_deserializer_VERSION}
    COMPATIBILITY AnyNewerVersion)

install(FILES "qbjs_deserializerConfig.cmake" "${CMAKE_CURRENT_BINARY_DIR}/qbjs_deserializerConfigVersion.cmake"
    DESTINATION lib/cmake/qbjs_deserializer)
