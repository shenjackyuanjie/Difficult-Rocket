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

from Difficult_Rocket.api.Exp.main import Error
from Difficult_Rocket.api.Exp.command import CommandError, CommandParseError, CommandQMarkPosError, \
    CommandQMarkConflict, CommandQMarkMissing, CommandQMarkPreMissing, CommandQMarkSufMissing
from Difficult_Rocket.api.Exp.unsupport import NoMoreJson5, Nope418ImTeapot, ThinkError, BrainError, \
    BrainTimeoutError, BigBrainError


class TexturesError(Error):
    """材质相关 error"""


class LanguageError(Error):
    """语言相关 error"""


class TestError(Error):
    """就像名字一样 用于测试的 error"""
