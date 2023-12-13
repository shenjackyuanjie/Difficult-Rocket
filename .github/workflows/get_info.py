#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
import sys
import rtoml
import io


sys.path.append(os.path.abspath(os.curdir))

try:
    stdout = sys.stdout
    sys.stdout = io.StringIO()
    from Difficult_Rocket import DR_status
    sys.stdout = stdout
except ImportError:
    raise

args = ["-env", "-github-dev"]


if sys.argv == [__file__]:  # 没有输入参数，直接输出默认信息并输出
    print(sys.version)
    from Difficult_Rocket.utils import tools

    # 重置窗口信息
    config_file = tools.load_file("./config/main.toml")
    config_file["window"]["width"] = 1024
    config_file["window"]["height"] = 768
    rtoml.dump(config_file, open("./config/main.toml", "w"))

elif os.path.abspath(os.curdir) in sys.path and "-env" in sys.argv:
    with open("./.github/workflows/env.ps1", encoding="utf-8", mode="w") as env_file:
        print(f'$env:DR_version = "{DR_status.DR_version}"', file=env_file)
        print(f'$env:Build_version = "{DR_status.Build_version}"', file=env_file)
elif os.path.abspath(os.curdir) in sys.path and "-github" in sys.argv:
    print(f"DR_version={DR_status.DR_version}")
    print(f"Build_version={DR_status.Build_version}")
