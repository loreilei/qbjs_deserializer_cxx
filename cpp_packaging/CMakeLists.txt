cmake_minimum_required(VERSION 3.23)

project(qbjs_deserializer VERSION 0.0.2)

find_package(Threads REQUIRED)

add_library(qbjs_deserializer SHARED
            ${CMAKE_SOURCE_DIR}/qbjs_deserializer/include/qbjs_deserializer/qbjs_deserializer.hpp
            ${CMAKE_SOURCE_DIR}/qbjs_deserializer/src/qbjs_deserializer.cpp
        )

set_property(TARGET qbjs_deserializer PROPERTY CXX_STANDARD 17)
set_property(TARGET qbjs_deserializer PROPERTY CMAKE_CXX_STANDARD_REQUIRED TRUE)
set_property(TARGET qbjs_deserializer PROPERTY CMAKE_SKIP_RPATH TRUE)

if (UNIX)
set(QBJS_DESERIALIZER_EXTRA_LINK_LIBRARIES
    dl
)
endif()

target_link_libraries(qbjs_deserializer
    PRIVATE
    ${CMAKE_SOURCE_DIR}/qbjs_deserializer/lib/libqbjs_deserializer_cxx.a
    ${CMAKE_SOURCE_DIR}/qbjs_deserializer/lib/libcxxbridge1.a
    Threads::Threads
    ${QBJS_DESERIALIZER_EXTRA_LINK_LIBRARIES}
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
