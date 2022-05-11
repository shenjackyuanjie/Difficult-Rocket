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

from .command import CommandParseError, CommandQuotationMarkError

__all__ = ['TexturesError',
           'LanguageError',
           'CommandError',
           'CommandParseError',
           'CommandQuotationMarkError',
           'TestError']


class Error(Exception):
    """基础 Exception"""
    pass


class TexturesError(Error):
    """材质相关 error"""
    pass


class CommandError(Error):
    """命令解析相关 error"""
    pass


class LanguageError(Error):
    """语言相关 error"""
    pass


class TestError(Error):
    """就像名字一样 用于测试的 error"""
    pass
