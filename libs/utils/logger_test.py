#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import inspect
from viztracer import VizTracer

import py_logger
from build import logger as c_logger

A_py_logger = py_logger.get_logger(name='client')
A_c_logger = c_logger.get_logger(name='client')

A_py_logger.info('aaaaa', frame=inspect.currentframe())
A_c_logger.info('aaaaa', frame=inspect.currentframe())
a_frame = inspect.currentframe()


def a_test(log: py_logger.Logger):
    log.info('123', frame=a_frame)


print('py_py')
py_logger.test_logger(A_py_logger)
print('py_c')
py_logger.test_logger(A_c_logger)
print('c_py')
c_logger.test_logger(A_py_logger)
print('c_c')
c_logger.test_logger(A_c_logger)
a_test(A_c_logger)
with VizTracer(output_file='loggers.json', file_info=True) as _:
    print('py_py')
    py_logger.test_logger(A_py_logger)
    print('py_c')
    py_logger.test_logger(A_c_logger)
    print('c_py')
    c_logger.test_logger(A_py_logger)
    print('c_c')
    c_logger.test_logger(A_c_logger)
