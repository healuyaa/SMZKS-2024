cmake_minimum_required(VERSION 3.5.0)
project(lab1 VERSION 0.1.0 LANGUAGES C CXX)

file(GLOB SOURCES    
    ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/include/*.hpp
)

include_directories(${CMAKE_SOURCE_DIR}/include)

add_executable(lab1 ${SOURCES})
