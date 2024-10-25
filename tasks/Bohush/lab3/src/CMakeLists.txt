cmake_minimum_required(VERSION 3.5.0)
project(lab3 VERSION 0.1.0 LANGUAGES C CXX)

file(GLOB SOURCES    
    ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/include/*.hpp
)

find_package(OpenSSL REQUIRED)

include_directories(${CMAKE_SOURCE_DIR}/include)

add_executable(lab3 ${SOURCES})
# add_executable(lab3 ./test.cpp)

target_link_libraries(lab3 PRIVATE OpenSSL::SSL OpenSSL::Crypto)

