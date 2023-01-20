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

from Difficult_Rocket import DR_runtime
from Difficult_Rocket.command import line

COMMAND = 'command'
SUB_COMMAND = 'sub_command'
INFO = 'info'
RUN = 'run'

DR_command = {
    'name':    'DR-root',
    'version': DR_runtime.DR_version,
    INFO:      'DR的自带命令解析树',
    COMMAND:   {
        INFO:        '这里是DR的根命令节点',
        RUN:         None,
        SUB_COMMAND: {
            'stop':    {
                INFO: '退出游戏',
                RUN:  None
            },
            'fps':     {
                INFO:        'FPS相关命令',
                RUN:         None,
                SUB_COMMAND: {
                    'log': {
                        INFO: '输出FPS信息',
                        RUN:  None
                    },
                    'min': {
                        INFO: '输出一段时间内最小fps',
                        RUN:  None
                    },
                    'max': {
                        INFO: '输出一段时间内最大FPS',
                        RUN:  None
                    }
                }
            },
            'default': {
                INFO: '重置一些设置'
            }
        }
    }
}

"""
abc <a> abc -> abc()
abc a abc -> bbb()
abc -> help('abc')
"""


# TODO 给爷做了他


class CommandTree:
    def __init__(self, command_tree_dict):
        self.command_tree_dict = command_tree_dict

    def parse(self, command: [line.CommandText, str]):
        pass
