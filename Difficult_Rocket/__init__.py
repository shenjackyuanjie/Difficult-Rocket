#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

from typing import Any

from libs.MCDR.version import Version

game_version = Version("0.6.2")
__version__ = game_version

DR_options = {
    'InputBox_use_TextEntry': False,
    'playing': False,
    'debugging': False
}

_DR_options_type = {
    'InputBox_use_TextEntry': bool,
    'playing': bool,
    'debugging': bool
}


def DR_option_type(config_name: str):
    if config_name in _DR_options_type:
        return _DR_options_type[config_name]
    return Any


if DR_options['playing']:
    from .utils import new_thread


    def think_it(something):
        return something


    @new_thread('think')
    def think(some_thing_to_think):
        gotcha = think_it(some_thing_to_think)
        return gotcha
