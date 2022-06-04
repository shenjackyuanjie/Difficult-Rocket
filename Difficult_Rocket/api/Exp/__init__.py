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

__all__ = ['TexturesError',
           'LanguageError',
           'TestError']


class Error(Exception):
    """基础 Exception"""
    def __bool__(self):
        return False


class TexturesError(Error):
    """材质相关 error"""


class LanguageError(Error):
    """语言相关 error"""


class TestError(Error):
    """就像名字一样 用于测试的 error"""
