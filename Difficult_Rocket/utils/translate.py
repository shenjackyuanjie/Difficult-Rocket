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

from typing import Union

from Difficult_Rocket.api.Exp import *
from Difficult_Rocket.utils import tools

"""
这部分代码使用了中文编程，why？
你觉得呢？
"""


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

    def __init__(self, language: str = 'zh-CN') -> None:
        self.语言 = language
        self.翻译结果 = tools.load_file(f'configs/lang/{language}.toml')
        self.默认翻译 = tools.load_file('configs/lang/zh-CN.toml')

    def __str__(self) -> str:
        return self.语言

    def __getitem__(self, item) -> Union[int, str, list, dict]:
        try:
            return self.翻译结果[item]
        except KeyError:
            try:
                return self.默认翻译[item]
            except KeyError:
                raise LanguageError(f'there\'s no key {item} in both {self.语言} and zh-CN')

    def __setitem__(self, key, value) -> None:
        if key == 'language' or key == 'lang':
            try:
                self.翻译结果 = tools.load_file(f'configs/lang/{value}.toml')
                self.语言 = value
            except FileNotFoundError:
                raise LanguageError(f'{value}\'s language toml file not found')
        else:
            raise NotImplementedError

    def set_language(self, language) -> None:
        try:
            self.翻译结果 = tools.load_file(f'configs/lang/{language}.toml')
            self.语言 = language
        except FileNotFoundError:
            raise LanguageError(f'{language}\'s language toml file not found')

    def lang(self, *args) -> Union[int, str, list, dict]:
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
                raise LanguageError(f'there\'s no key {args} in both {self.语言} and zh-CN')

    def 翻译(self, *args) -> Union[int, str, list, dict]:
        return self.lang(args)


tr = Lang('zh-CN')

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
