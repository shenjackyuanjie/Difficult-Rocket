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



from .api import *

__all__ = [
    'new_thread',
    'Delivery',
    'config'
]


@new_thread('think')
def think(some_thing_to_think):
    gotcha = 'think_result'
    return gotcha
