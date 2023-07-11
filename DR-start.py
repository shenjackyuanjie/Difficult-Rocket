#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
import sys
import time

from pathlib import Path

hi = """Difficult Rocket is writen by shenjackyuanjie
email: 3695888@qq.com or shyj3695888@163.com
QQ: 3695888"""


def print_path() -> None:
    print(f'{__file__=}')
    print(f'{sys.path=}')
    print(f'{sys.path[0]=}')
    print(f'{sys.argv[0]=}')
    print(f'{Path.cwd()=}')
    print(f'{Path(__file__).absolute()=}')


def modify_path() -> None:
    os.chdir(Path(__file__))  # 将运行路径切换到文件位置 防止bug
    sys.path.append(f'./Difficult_Rocket')  # 添加local path
    sys.path.append(f'./libs')  # 添加 libs path


def start(start_time_ns: int) -> None:
    from Difficult_Rocket import main
    from Difficult_Rocket.runtime import DR_runtime
    DR_runtime.start_time_ns = start_time_ns

    try:
        main_game = main.Game()
    except Exception as exp:



if __name__ == '__main__':
    print(hi, f"\n{time.ctime()}")  # hi！
    # 记录启动信息
    start_time_ns = time.time_ns()
    print_path()
    modify_path()
    start(start_time_ns)


