#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import os
import sys
import time
import cProfile
import traceback

hi = """Difficult Rocket is writen by shenjackyuanjie
email: 3695888@qq.com or shyj3695888@163.com
QQ: 3695888"""

errors = {
    'TestError':      '游戏正在调试中，某处引发了一个 TestError，不是bug造成的原因',
    'AssertionError': '游戏的某处检查未通过，情报告issue',
    'error.unknown':  '游戏报错了，现在输出报错信息，请报告issue',
    'error.happen':   '游戏出现了一个报错！正在处理'
}

def print_path() -> None:
    print(f'{__file__=}')
    print(f'{sys.path=}')
    print(f'{sys.path[0]=}')
    print(f'{sys.argv[0]=}')
    print(f'{os.getcwd()=}')
    print(f'{os.path.abspath(__file__)=}')
    print(f'{os.path.realpath(__file__)=}')
    print(f'{os.path.split(os.path.split(os.path.realpath(__file__))[0])=}')
    # 输出一遍大部分文件位置相关信息 以后可能会加到logs里


def modify_path() -> None:
    file_path = os.path.split(os.path.realpath(__file__))[0]
    os.chdir(file_path)  # 将运行路径切换到文件位置 防止bug
    sys.path.append(f'{file_path}/Difficult_Rocket')  # 添加local path
    sys.path.append(f'{file_path}/libs')  # 添加 libs path


if __name__ == '__main__':
    print(hi)  # hi！
    # 记录启动信息
    start_time_ns = time.time_ns()
    start_time_perf_ns = time.perf_counter_ns()
    print_path()
    modify_path()
    

