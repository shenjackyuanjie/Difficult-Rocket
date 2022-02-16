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

"""
这里是所有客户端 mod 加载器的装饰器实现
可以实现类似

from Difficult_Rocket.mods.client import KeyBinding


@KeyBinding()

"""


def KeyBinding(func):
    """
    客户端键盘事件传递装饰器
    """

    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

    return wrapper
