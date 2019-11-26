cmake_minimum_required(VERSION 3.14)

project(RemoteVim)


find_package(spdlog REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
add_executable(RemoteVim src/Host.cpp src/Session.cpp src/RemoteCommand.cpp main.cpp)
target_link_libraries(RemoteVim PRIVATE spdlog::spdlog)