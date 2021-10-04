#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

from typing import Union

from Difficult_Rocket.api import tools
from Difficult_Rocket.api.Exp import *

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

    def __init__(self, language: str = 'zh-CN'):
        self.language = language
        self.翻译结果 = tools.load_file(f'configs/lang/{language}.json5')
        self.默认翻译 = tools.load_file('configs/lang/zh-CN.json5')

    def __str__(self) -> str:
        return self.language

    def __getitem__(self, item):
        try:
            return self.翻译结果[item]
        except KeyError:
            try:
                return self.默认翻译[item]
            except KeyError:
                raise LanguageError(f'there\'s no key {item} in both {self.language} and zh-CN')

    def __setitem__(self, key, value):
        if key == 'language' or key == 'lang':
            try:
                self.翻译结果 = tools.load_file(f'configs/lang/{value}.json5')
                self.language = value
            except FileNotFoundError:
                raise LanguageError(f'{value}\'s language json5 file not found')
        else:
            raise NotImplementedError

    def set_language(self, language):
        try:
            self.翻译结果 = tools.load_file(f'configs/lang/{language}.json5')
            self.language = language
        except FileNotFoundError:
            raise LanguageError(f'{language}\'s language json5 file not found')

    def lang(self, *args) -> Union[int, str, list]:
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
                raise LanguageError(f'there\'s no key {args} in both {self.language} and zh-CN')

    def 翻译(self, *args):
        self.lang(args)


tr = Lang('zh-CN')

# font's value

HOS = 'HarmonyOS_Sans'
HOS_S = 'HarmonyOS_Sans_SC'
HOS_T = 'HarmonyOS_Sans_TC'
HOS_I = 'HarmonyOS_Sans_Italic'
HOS_C = 'HarmonyOS_Sans_Condensed'
HOS_CI = 'HarmonyOS_Sans_Condensed_Italic'
HOS_NA = 'HarmonyOS_Sans_Naskh_Arabic'
HOS_NAU = 'HarmonyOS_Sans_Naskh_Arabic_UI'

鸿蒙字体 = HOS
鸿蒙简体 = HOS_S
鸿蒙繁体 = HOS_T
鸿蒙斜体 = HOS_I
鸿蒙窄体 = HOS_C
鸿蒙斜窄体 = HOS_CI
鸿蒙阿拉伯 = HOS_NA
鸿蒙阿拉伯UI = HOS_NAU
