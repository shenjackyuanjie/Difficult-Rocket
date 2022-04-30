#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""
import cProfile
import time


def run():
    start_time = time.perf_counter_ns()
    print(*[x for x in range(1, 100000) if sum([int(i)**len(str(x)) for i in str(x)]) == x])
    print(time.perf_counter_ns() - start_time)


cProfile.run("run()")

