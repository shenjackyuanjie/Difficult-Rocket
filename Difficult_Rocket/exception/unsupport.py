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
from Difficult_Rocket.exception import BaseError, BaseRuntimeError

__all__ = [
    'NoMoreJson5',
    'Nope418ImATeapot',
    'ThinkError',
    'BrainError',
    'BigBrainError',
    'GrammarError'
]


class NoMoreJson5(BaseError):
    """说什么我也不用Json5了！"""


class Nope418ImATeapot(BaseError):
    """我只是个茶壶而已，我不能煮咖啡！"""


class ThinkError(BaseError):
    """进不去，进不去，怎么想都进不去！"""


class BrainError(BaseError):
    """clever brain.png"""


class BigBrainError(BrainError):
    """bigbrain.png"""


class BrainTimeoutError(BrainError, ThinkError):
    """脑子····超时·······················啦！"""


class GrammarError(BaseRuntimeError):
    """嘿NMD语法！"""
