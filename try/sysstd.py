#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import sys


with sys.stdout as f:
    print('aaaaa', file=f, flush=True)

with sys.__stdout__ as f:
    print(f.readlines())
