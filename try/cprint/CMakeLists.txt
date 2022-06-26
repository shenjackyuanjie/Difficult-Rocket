cmake_minimum_required(VERSION 3.22)
project(cprint VERSION 0.0.1 LANGUAGES C)
# 环境
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_C_STANDARD 99)
# 编译选项
add_compile_options(-O3)
add_compile_options(-Wall)
add_compile_options(-Werror)
#add_compile_options(-shared)
#add_compile_options(-o ../../cprint.dll)
# 加一下py3.8的 path
include_directories(.)
include_directories(C:\\Users\\shenjack.SHENJACK-5600X\\AppData\\Local\\Programs\\Python\\Python38\\include\\.)
# 编译可执行
#add_executable(cprint cprint.c)
# 编译动态链接库
add_library(cprint cprint.c)
file(COPY cmake-build-debug/libcprint.a DESTINATION /cprint.dll)

