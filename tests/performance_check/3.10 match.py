"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import time
import random


def match_test():
    start_time = time.perf_counter_ns()
    for x in range(times):
        get = random.randint(1, 10)
        match get:
            case 1:
                continue
            case 2:
                continue
            case 3:
                continue
            case 4:
                continue
            case 5:
                continue
            case 6:
                continue
            case 7:
                continue
            case 8:
                continue
            case 9:
                continue
            case _:
                continue
    end_time = time.perf_counter_ns()
    print(f'match {end_time-start_time=} {times=}')


def if_test():
    start_time = time.perf_counter_ns()
    for x in range(times):
        get = random.randint(1, 10)
        if get == 1:
            continue
        elif get == 2:
            continue
        elif get == 3:
            continue
        elif get == 4:
            continue
        elif get == 5:
            continue
        elif get == 6:
            continue
        elif get == 7:
            continue
        elif get == 8:
            continue
        elif get == 9:
            continue
        else:
            continue
    end_time = time.perf_counter_ns()
    print(f'if    {end_time-start_time=} {times=}')


for x in range(8):
    times = 10 ** x
    match_test()
    if_test()
    print('')
