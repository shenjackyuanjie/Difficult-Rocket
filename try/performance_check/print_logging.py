#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie
#  All rights reserved
#  -------------------------------


import logging
import time


def a_print(name):
    print(name)


def a_log(name):
    logging.info(name)


logging.basicConfig(level=logging.DEBUG)

start_print = time.perf_counter()
for x in range(100000):
    a_print('aaa')
end_print = time.perf_counter()

start_log = time.perf_counter()
for x in range(100000):
    a_log('aaa')
print(end_print - start_print)
print(time.perf_counter() - start_log)
