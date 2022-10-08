cmake_minimum_required(VERSION 3.23)
project(qbjsDeserializerTest)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_set_find_paths()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Don't pulluate the RPATH with conan dependencies
# instead copy all shared deps in ../lib
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH FALSE)

if (UNIX)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")
    if (APPLE)
        set(CMAKE_INSTALL_RPATH "@executable_path/../lib")
    else()
        set(CMAKE_INSTALL_RPATH "$ORIGIN/../lib")
        set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,--disable-new-dtags")
    endif()
endif()

 # Turn all the warnings into errors
if (MSVC)
	set(EXTRA_CXX_FLAGS "${EXTRA_CXX_FLAGS} /WX")
else()
	set(EXTRA_CXX_FLAGS "${EXTRA_CXX_FLAGS} -Werror")
endif()

find_package(qbjs_deserializer 0.0.4 REQUIRED)

add_executable(testApp src/main.cpp)
target_link_libraries(testApp PRIVATE QBJS_DESERIALIZER::qbjs_deserializer)
install(TARGETS testApp RUNTIME DESTINATION "bin")
