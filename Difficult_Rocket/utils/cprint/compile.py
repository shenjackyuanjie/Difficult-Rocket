
import os

# include 目录
include_paths = ["C:\\Users\\shenjack.SHENJACK-5600X\\AppData\\Local\\Programs\\Python\\Python38\\include\\."]

# 编译选项
compile_options = {
    "-shared": None,
    "-O3": None,
    "-Wall": None,
    "-Werror": None,
    "-o": "./py_cprint.dll"
}

include_command = "-I "

# 处理 include 目录命令
for path in include_paths:
    include_command = "{}, {}".format(include_command, path)
else:
    if len(include_paths) != 0:
        include_command = include_command[:3] + include_command[4:]

compile_option_command = ""

# 处理编译选项
for option, key in compile_options.items():
    if key is None:
        compile_option_command = "{} {} ".format(compile_option_command, option)
    else:
        compile_option_command = "{} {} {}".format(compile_option_command, option, key)

print(include_command, compile_option_command)

compile_command = "gcc.exe ./py_cprint.c {}{}".format(include_command, compile_option_command)

print(compile_command)

os.system(compile_command)

