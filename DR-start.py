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

if __name__ == '__main__':
    # 记录启动信息
    start_time_ns = time.time_ns()
    start_time_perf_ns = time.perf_counter_ns()
    