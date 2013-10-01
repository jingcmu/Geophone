cmake_minimum_required(VERSION 2.8)

project(Geophone)

include_directories(
    native/include
)

set(geophone-src
    native/src/analyze.c
    native/src/geophone_module.c
)

set(libgeophone_module
    GeophoneModule
)

add_library(${libgeophone_module} SHARED ${geophone-src})

set_target_properties(${libgeophone_module} PROPERTIES
        COMPILE_FLAGS "-Wall -fPIC"
)
