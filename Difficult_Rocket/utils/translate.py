#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie <3695888@qq.com>
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import inspect
# import dataclasses

from typing import Union, Tuple, Any, Type, List, Dict, Hashable

from Difficult_Rocket import DR_runtime, DR_option
from Difficult_Rocket.utils import tools
from Difficult_Rocket.exception.language import *

"""
这部分代码使用了中文编程，why？
你觉得呢？
"""

class Translated:
    def __init__(self, value: Union[list, tuple, dict, str], raise_error: bool = False):
        self.value = value
        self.raise_error = raise_error
        self.item_names = []

    def __getattr__(self, item):
        if hasattr(object, item):
            return getattr(object, item)
        self.item_names.append(item)
        return self

    def __getitem__(self, item):
        self.item_names.append(item)
        return self

    def __str__(self):
        if not self.item_names:
            return self.value
        else:
            return f'{self.value}.{".".join(self.item_names)}'


class Translating:
    def __init__(self, value: Union[Dict[str, Any], list, tuple], raise_error: bool = False, get_list: list = None):
        self.value: Union[Dict[str, Any], list, tuple] = value
        self.raise_error = raise_error
        self.get_list = get_list or []

    def __getitem__(self, item: Union[str, Hashable]) -> Union["Translating", Translated]:
        cache_get_list = self.get_list.copy()
        cache_get_list.append(item)
        try:
            cache = self.value[item]
        except (KeyError, TypeError):
            if DEBUG_PRINT:
                frame = inspect.currentframe()
                last_frame = frame.f_back
                if last_frame.f_code == self.__getattr__.__code__:
                    last_frame = last_frame.f_back
                call_info = f'Translate Not Found at {last_frame.f_code.co_name} by {".".join(cache_get_list)} at:' \
                            f'{last_frame.f_code.co_filename}:{last_frame.f_lineno}'
                print(call_info)
            if not self.raise_error:
                return Translated('.'.join(cache_get_list), raise_error=False)
            else:
                raise GetItemError(item_names=cache_get_list)
        return Translating(value=cache, raise_error=self.raise_error, get_list=cache_get_list)

    def __getattr__(self, item: Union[str, Hashable]) -> Union["Translating", Translated]:
        if hasattr(object, item):
            return getattr(object, item)
        return self.__getitem__(item)

    def __str__(self):
        return str(self.value)


class Tr:
    """
    我不装了，我就抄了tr
    GOOD
    """

    def __init__(self, language: str = DR_runtime.language):
        self.language_name = language
        self.translates: Dict = tools.load_file(f'configs/lang/{language}.toml')
        self.default_translate: Dict = tools.load_file(f'configs/lang/{DR_runtime.default_language}.toml')
        self.不抛出异常 = False

    def __call__(self):
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
        self.translates = tools.load_file(f'configs/lang/{DR_runtime.language}.toml')
        self.default_translates = tools.load_file('configs/lang/zh-CN.toml')
        self.直接返回原始数据 = True

    def __str__(self) -> str:
        return DR_option.language

    def __getitem__(self, item) -> Union[int, str, list, dict]:
        try:
            return self.translates[item]
        except KeyError:
            try:
                return self.default_translates[item]
            except KeyError:
                raise TranslateKeyNotFound(f'there\'s no key {item} in both {DR_option.language} and zh-CN')

    def lang(self, *args) -> Union[int, str, list, dict]:
        # frame = inspect.currentframe()
        # # print("调用当前log的文件名:", frame.f_back.f_code.co_filename)
        # objprint.objprint(frame.f_back.f_code,
        #                   honor_existing=False,
        #                   depth=2)
        try:
            result = self.translates
            for option in args:
                result = result[option]
            return result
        except KeyError:
            try:
                result = self.default_translates
                for option in args:
                    result = result[option]
                return result
            except KeyError as e:
                if self.直接返回原始数据:
                    return args
                raise TranslateKeyNotFound(f'there\'s no key {args} in both {DR_option.language} and zh-CN') from e

    def 翻译(self, *args) -> Union[int, str, list, dict]:
        return self.lang(args)

    def _update_lang(self) -> str:
        """
        用于更新语言(内部调用)
        :return: 设置完成后的语言
        """
        self.translates = tools.load_file(f'configs/lang/{DR_option.language}.toml')
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

得意黑 = '得意黑'
