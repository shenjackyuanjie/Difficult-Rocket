#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

import os
import sys
import time
import psutil
import ctypes
import random
import cProfile


class PartData_C(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double),
                ("y", ctypes.c_double),
                ("vx", ctypes.c_double),
                ("vy", ctypes.c_double)]


class PartData_Py:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy


def count_time(func):
    def int_time():
        start_time = time.perf_counter()
        func()
        over_time = time.perf_counter()
        total_time = over_time - start_time
        print("程序运行了%s秒" % total_time)

    return int_time


test_times = 1000


def count_info(func):
    def float_info():
        pid = os.getpid()
        p = psutil.Process(pid)
        info_start = p.memory_full_info().uss / 1024
        func()
        info_end = p.memory_full_info().uss / 1024
        print("程序占用了内存" + str(info_end - info_start) + "KB")
        print(info_start, info_end)

    return float_info


@count_time
@count_info
def c_class_test():
    class_list = [PartData_C(x=random.random(), y=random.random(), vx=random.random(), vy=random.random()) for x in range(test_times)]
    for x in class_list:
        x.x = random.random()
        x.y = random.random()
        x.vx = random.random()
        x.vy = random.random()
    print(sys.getsizeof(class_list, 1), '\n')


@count_time
@count_info
def py_class_test():
    class_list = [PartData_Py(x=random.random(), y=random.random(), vx=random.random(), vy=random.random()) for x in range(test_times)]
    for x in class_list:
        x.x = random.random()
        x.y = random.random()
        x.vx = random.random()
        x.vy = random.random()
    print(sys.getsizeof(class_list, 1), '\n')


# gc.disable()

cProfile.run('c_class_test()', sort='calls')
# time.sleep(1)
cProfile.run('py_class_test()', sort='calls')
