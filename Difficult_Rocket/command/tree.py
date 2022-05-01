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

from Difficult_Rocket import game_version
from Difficult_Rocket.command import line



command_tree = {
    'name':        'DR-root',
    'version':     game_version,
    'information': 'DR这一部分的代码还TM是复制我之前写的屑Census',
    'commands':    {
        'info':        '啊啊啊啊',
        'hint':        '然而并没有什么隐藏信息(确信)',
        'run':         '{app_name} help',
        'sub_command': {
            'stop':   {
                'info': '停止游戏',
                'hint': 'g 你就在看着我呢~',
                'run':  '{command}',
            },
            'default': {
                'info': '重置游戏',
                'hint': 'g 获得成就:我重置我自己',
                'run':  '{command}',
            },
            'fps':  {
                'sub_command': {
                    'log':  {
                        'info': '输出FPS日志',
                        'hint': 'rub 本操作会覆盖现有数据，所以请自行输入命令',
                        'run':  '{command}',
                    },
                    'max':  {
                        'info': '输出最大FPS',
                        'hint': 'ub 提醒:这个操作会覆盖文件数据(虽说其实没啥事)',
                        'run':  '{command}',
                    },
                    'mix': {
                        'info': '输出最小FPS',
                        'hint': '获得成就:我打印了分数',
                        'run':  '{command}',
                    }
                }
            }
        }
    }
}
# TODO 给爷做了他


class CommandTree:
    def __init__(self, command_tree_dict):
        self.command_tree_dict = command_tree_dict

    def parse(self, command: line.CommandText):
        pass
