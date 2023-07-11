#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
import sys
import time
import traceback
import threading

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
    from Difficult_Rocket import crash, DR_status
    from Difficult_Rocket.runtime import DR_runtime
    from Difficult_Rocket.exception import TestError
    DR_runtime.start_time_ns = start_time_ns
    try:
        from Difficult_Rocket import main
        main_game = main.Game()
        main_game.start()
        if DR_status.crash_report_test:
            raise TestError('debug crash test')
    except:
        trace = traceback.format_exc()
        crash.create_crash_report(trace)
        crash.write_info_to_cache(sys.stdout)
    print(crash.all_thread)
    print(crash.all_process)
    for a_thread in threading.enumerate():
        print(a_thread)
        if a_thread.is_alive() and a_thread != threading.current_thread() and a_thread != threading.main_thread():
            a_thread.join(2)  # wait for 2 sec
    import pyglet
    pyglet.app.exit()  # make sure that pyglet has stopped


def main() -> int:
    print(hi, f"\n{time.ctime()}")  # hi！
    # 记录启动信息
    start_time_ns = time.time_ns()
    print_path()
    modify_path()
    start(start_time_ns)
    return 0


if __name__ == '__main__':
    sys.exit(main())
