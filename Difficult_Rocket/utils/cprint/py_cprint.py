#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import timeit
import time
from build import pycprint


time.sleep(1)
cpyprint = timeit.timeit('pycprint.print("啊啊")', number=100000, globals=globals())
pyprint = timeit.timeit('print("啊啊")', number=100000, globals=globals())

print(cpyprint, pyprint, pyprint - cpyprint)
time.sleep(10)

pycprint.print("a啊 a\n")
pycprint.print("a啊采购好难过 a\n")
print()
#
pycprint.printf("a啊a\n", "aaa", "aaa", end='')

print()

pycprint.printf()

pycprint.printf("aaa\n", "aaa", "aaa")
