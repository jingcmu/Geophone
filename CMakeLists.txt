cmake_minimum_required(VERSION 2.8)

project(Geophone)

include_directories(
    native/include
)

set(geophone-src
    native/src/analyze.c
    native/src/geophone.c
)

set(libgeophone
    Geophone
)

add_library(${libgeophone} SHARED ${geophone-src})

set_target_properties(${libgeophone} PROPERTIES
        COMPILE_FLAGS "-Wall -fPIC"
)
