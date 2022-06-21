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

from libs.MCDR.version import Version

game_version = Version("0.6.2")
__version__ = game_version

DR_options = {
    'InputBox_use_TextEntry': False,
    'playing': False
}

_DR_options_type = {
    'InputBox_use_TextEntry': bool,
    'playing': bool
}

if DR_options['playing']:
    from .api import new_thread


    def think_it(something):
        return something


    @new_thread('think')
    def think(some_thing_to_think):
        gotcha = think_it(some_thing_to_think)
        return gotcha
