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

import inspect
import objprint

from typing import Union

from Difficult_Rocket import DR_runtime, DR_option
from Difficult_Rocket.utils import tools
from Difficult_Rocket.exception.language import *


"""
这部分代码使用了中文编程，why？
你觉得呢？
"""


class Tr:
    """
    我不装了，我就复刻tr
    """
    def __init__(self):
        self.config_regs = {}

    def add_config(self, configs: dict) -> None:
        frame = inspect.currentframe()
        self.config_regs[frame.f_back.f_code.co_filename] = configs

    def __call__(self, *args, **kwargs):
        frame = inspect.currentframe()
        if frame.f_back.f_code.co_filename in self.config_regs:
            ...
        else:
            ...




class Lang:
    """
    用于创建一个对应语言的翻译类
    感谢Fallen的MCDR提供idea
    https://github.com/Fallen-Breath/MCDReforged
    可以用
    lang['language'] = 'abc' 或
    lang['lang'] = 'abc'
    的方式直接更改并刷新翻译
    用
    lang.lang(xxx, xxx)来获取翻译过的值
    """

    def __init__(self) -> None:
        self.翻译结果 = tools.load_file(f'configs/lang/{DR_runtime.language}.toml')
        self.默认翻译 = tools.load_file('configs/lang/zh-CN.toml')
        self.直接返回原始数据 = True

    def __str__(self) -> str:
        return DR_option.language

    def __getitem__(self, item) -> Union[int, str, list, dict]:
        try:
            return self.翻译结果[item]
        except KeyError:
            try:
                return self.默认翻译[item]
            except KeyError:
                raise TranslateKeyNotFound(f'there\'s no key {item} in both {DR_option.language} and zh-CN')

    def lang(self, *args) -> Union[int, str, list, dict]:
        # frame = inspect.currentframe()
        # # print("调用当前log的文件名:", frame.f_back.f_code.co_filename)
        # objprint.objprint(frame.f_back.f_code,
        #                   honor_existing=False,
        #                   depth=2)
        try:
            结果 = self.翻译结果
            for 选项 in args:
                结果 = 结果[选项]
            return 结果
        except KeyError:
            try:
                结果 = self.默认翻译
                for 选项 in args:
                    结果 = 结果[选项]
                return 结果
            except KeyError:
                if self.直接返回原始数据:
                    return args
                raise TranslateKeyNotFound(f'there\'s no key {args} in both {DR_option.language} and zh-CN')

    def 翻译(self, *args) -> Union[int, str, list, dict]:
        return self.lang(args)

    def _update_lang(self) -> str:
        """
        用于更新语言(内部调用)
        @return: 设置完成后的语言
        """
        self.翻译结果 = tools.load_file(f'configs/lang/{DR_option.language}.toml')
        return DR_option.language


if not __name__ == '__main__':
    tr = Lang()

# font's value

HOS = 'HarmonyOS Sans'
HOS_S = 'HarmonyOS Sans SC'
HOS_T = 'HarmonyOS Sans TC'
HOS_C = 'HarmonyOS Sans Condensed'

鸿蒙字体 = HOS
鸿蒙简体 = HOS_S
鸿蒙繁体 = HOS_T
鸿蒙窄体 = HOS_C

CC = 'Cascadia Code'
CM = 'Cascadia Mono'
CCPL = 'Cascadia Code PL'
CMPL = 'Cascadia Mono PL'

微软等宽 = CC
微软等宽无线 = CM
微软等宽带电线 = CCPL
微软等宽带电线无线 = CMPL
