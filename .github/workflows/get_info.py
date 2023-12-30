#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
import sys
import tomlkit
import io


sys.path.append(os.path.abspath(os.curdir))

is_github = "-github" in sys.argv

if is_github:
    stdout = sys.stdout
    sys.stdout = io.StringIO()

try:
    from Difficult_Rocket import DR_status
except ImportError:
    raise

if is_github:
    sys.stdout = stdout


if sys.argv == [__file__]:  # 没有输入参数，直接输出默认信息并输出
    print(sys.version)
    from Difficult_Rocket.utils import tools

    # 重置窗口信息
    config_file = tools.load_file("./config/main.toml")
    config_file["window"]["width"] = 1024
    config_file["window"]["height"] = 768
    tomlkit.dump(config_file, open("./config/main.toml", "w"))

elif os.path.abspath(os.curdir) in sys.path and "-github" in sys.argv:
    print(f"DR_version={DR_status.DR_version}")
    print(f"Build_version={DR_status.Build_version}")
