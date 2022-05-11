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

from . import CommandError


class CommandParseError(CommandError):
    """命令解析时出现错误"""
    pass


class CommandQuotationMarkError(CommandParseError):
    """命令中,引号位置不正确
    例如： /command "aabcc "awdawd
    """
    pass
