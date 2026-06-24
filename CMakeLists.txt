cmake_minimum_required(VERSION 3.19)
project(dread CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# Use response files when linking objects because of the large number of source files
set(CMAKE_CXX_USE_RESPONSE_FILE_FOR_OBJECTS ON)
if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
  add_compile_options(-fdiagnostics-color=always)
elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
  add_compile_options(-fcolor-diagnostics)
  # Required to silence "unused argument" warnings for -stdlib=libc++ when using distcc
  add_compile_options(-Wno-unused-command-line-argument)
  # Required to fix source paths in debug info when using distcc
  add_compile_options(-fdebug-prefix-map=/tmp=${CMAKE_CURRENT_BINARY_DIR})
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

file(GLOB_RECURSE SOURCES_GAME CONFIGURE_DEPENDS 
${PROJECT_SOURCE_DIR}/src/*.cpp ${PROJECT_SOURCE_DIR}/src/*.c 
${PROJECT_SOURCE_DIR}/src/*.hpp ${PROJECT_SOURCE_DIR}/src/*.h)

add_executable(dread ${SOURCES_GAME})
target_include_directories(dread PRIVATE "includes/")
target_compile_definitions(dread PRIVATE NON_MATCHING)
target_compile_options(dread PRIVATE -fno-rtti -fno-exceptions)
target_compile_options(dread PRIVATE -fno-strict-aliasing)
target_compile_options(dread PRIVATE -Wall -Wextra -Wdeprecated)
target_compile_options(dread PRIVATE -Wno-unused-parameter -Wno-unused-private-field)
target_compile_options(dread PRIVATE -Wno-invalid-offsetof)
target_compile_options(dread PRIVATE -Wextra-semi)

set(NN_SDK 4.4.0)
set(NN_WARE 1.6.1)
set(NN_SDK_TYPE "Release")

add_subdirectory("lib/NintendoSDK")

add_subdirectory("lib/agl")

add_subdirectory("lib/sead")

target_link_libraries(dread PUBLIC
    sead
    NintendoSDK
    agl
)