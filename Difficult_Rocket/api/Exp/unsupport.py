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


class NoMoreJson5(Error):
    """说什么我也不用Json5了！"""


class Nope418ImTeapot(Error):
    """我只是个茶壶而已，我不能煮咖啡！"""


class ThinkError(Error):
    """进不去，进不去，怎么想都进不去！"""


class BrainError(Error):
    """clever brain.png"""


class BigBrainError(BrainError):
    """bigbrain.png"""


class BrainTimeoutError(BrainError, ThinkError):
    """脑子····超时·······················啦！"""
