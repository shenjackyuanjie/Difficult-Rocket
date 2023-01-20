#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""
from Difficult_Rocket.exception import BaseRuntimeError

__all__ = [
    "CommandError",
    "CommandParseError",
    "CommandQMarkMissing",
    "CommandQMarkPosError",
    "CommandQMarkConflict",
    "CommandQMarkSufMissing",
    "CommandQMarkPreMissing"
]


class CommandError(BaseRuntimeError):
    """命令解析相关 error"""


class CommandParseError(CommandError):
    """命令解析时出现错误"""


# QMark -> Quotation marks
# Pos -> Position

class CommandQMarkPosError(CommandParseError):
    """命令中,引号位置不正确
    例如： /command "aabcc "awdawd"""


class CommandQMarkMissing(CommandParseError):
    """命令中引号缺失
    例如: /command "aawwdawda awdaw """


class CommandQMarkConflict(CommandParseError):
    """命令中引号位置冲突
    例如: /command "aaaa "aaaa aaaa"""
    first_qmark_pos = None
    conflict_qmark_pos = None


class CommandQMarkPreMissing(CommandQMarkMissing):
    """命令中 前面的引号缺失
    例如: /command aaaa" aaaaaa"""
    suf_qmark_pos = None


class CommandQMarkSufMissing(CommandQMarkMissing):
    """命令中 后面的引号缺失(引号未闭合)
    例如: /command "aaaawaa some command"""
    pre_qmark_pos = None
