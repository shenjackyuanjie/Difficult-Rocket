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


class BaseError(Exception):
    """基本 exp"""

    def __bool__(self) -> bool:
        return False


class BaseRuntimeError(RuntimeError):
    """基本 runtime exp"""

    def __bool__(self) -> bool:
        return False


class TestError(BaseRuntimeError):
    """在 test 啦"""


