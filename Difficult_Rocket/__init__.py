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

version = '0.6.2'
__version__ = version


playing = False

if playing:
    from .api import new_thread

    @new_thread('think')
    def think(some_thing_to_think):
        gotcha = 'think_result'
        return gotcha
