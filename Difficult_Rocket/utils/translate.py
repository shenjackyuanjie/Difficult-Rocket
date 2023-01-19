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

from dataclasses import dataclass
from typing import Union, Tuple, Any, Type, List, Dict, Hashable, Optional

from Difficult_Rocket import DR_runtime, DR_option
from Difficult_Rocket.utils import tools
from Difficult_Rocket.exception.language import *


@dataclass
class TranslateConfig:
    raise_error: bool = False  # 引用错误时抛出错误
    crack_normal: bool = False  # 出现错误引用后 将引用到的正确内容替换为引用路径
    insert_crack: bool = True  # 加入引用的错误内容
    is_final: bool = False  # 是否为最终内容
    keep_get: bool = True  # 引用错误后是否继续引用
    always_copy: bool = False  # 是否一直新建 Translate (为 True 会降低性能)

    def set(self, item: str, value: bool) -> 'TranslateConfig':
        assert getattr(self, item, None) is not None, f'Config {item} is not in TranslateConfig'
        assert type(value) is bool
        setattr(self, item, value)
        return self

    def __copy__(self) -> 'TranslateConfig':
        return TranslateConfig(raise_error=self.raise_error,
                               crack_normal=self.crack_normal,
                               insert_crack=self.insert_crack,
                               is_final=self.is_final,
                               keep_get=self.keep_get,
                               always_copy=self.always_copy)

    def copy(self) -> 'TranslateConfig':
        return self.__copy__()


key_type = Union[str, int, Hashable]


class Translates:
    name = 'Translate'

    def __init__(self, value: Union[Dict[str, Any], list, tuple, str],
                 config: Optional[TranslateConfig] = None,
                 get_list: Optional[List[Tuple[bool, str]]] = None):
        """ 一个用于翻译的东西
        :param value: 翻译键节点
        :param config: 配置
        :param get_list: 获取列表
        """
        self.value: Union[Dict[str, Any], list, tuple] = value
        self.config = config or TranslateConfig()
        self.get_list = get_list or []

    def set_conf_(self, option: Union[str, TranslateConfig],
                  value: Optional[Union[bool, List[str]]] = None) -> 'Translates':
        assert isinstance(option, (TranslateConfig, str))
        if isinstance(option, TranslateConfig):
            self.config = option
            return self
        self.config.set(option, value)
        return self

    def _raise_no_value(self, e: Exception, item: key_type):
        if self.config.raise_error:
            raise TranslateKeyNotFound(self.value, [x[1] for x in self.get_list]) from None
        elif DR_option.report_translate_no_found:
            frame = inspect.currentframe()
            if frame is not None:
                frame = frame.f_back
                if frame.f_back.f_code is not self.__getattr__.__code__:
                    frame = frame.f_back
                frame = f'call at {frame.f_code.co_filename}:{frame.f_lineno}'
            else:
                frame = 'but No Frame environment'
            raise_info = f"{self.name} Cause a error when getting {item} {frame}"
            print(raise_info)

    def __getitem__(self, item: key_type) -> "Translates":
        try:
            cache_value = self.value[item]
            if isinstance(cache_value, (int, str,)):
                self.config.is_final = True
            self.get_list.append((True, item))
            if self.config.always_copy:
                return Translates(value=cache_value, config=self.config, get_list=self.get_list)
            self.value = cache_value
            return self
        except (KeyError, TypeError, AttributeError) as e:
            self.get_list.append((False, item))
            self._raise_no_value(e, item)
            if not self.config.keep_get:
                self.config.is_final = True

    def copy(self):
        return self.__copy__()

    def __copy__(self) -> 'Translates':
        return Translates(value=self.value, config=self.config, get_list=self.get_lists)

    def __getattr__(self, item: key_type) -> "Translates":
        # 实际上我这里完全不需要处理正常需求，因为 __getattribute__ 已经帮我处理过了
        return self.__getitem__(item)

    def __str__(self):
        if self.config.crack_normal:
            return f'{".".join(f"{gets[1]}({gets[0]})" for gets in self.get_list)}'
        elif self.config.insert_crack:
            return f'{self.value}.{".".join(gets[1] for gets in self.get_list if not gets[0])}'
        return self.value


class Tr:
    """
    我不装了，我就抄了tr(实际上没啥关系)
    GOOD
    """

    def __init__(self, language: str = None, config: Optional[TranslateConfig] = None):
        """
        诶嘿，我抄的MCDR
        :param language: Tr 所使用的的语言
        :param config: 配置
        """
        self.language_name = language or DR_runtime.language
        self.translates: Dict[str,] = tools.load_file(f'configs/lang/{self.language_name}.toml')
        self.default_translate: Dict = tools.load_file(f'configs/lang/{DR_runtime.default_language}.toml')
        self.default_config = config or TranslateConfig()
        self.translates_cache = Translates(value=self.translates, config=TranslateConfig().copy())

    def __getattr__(self, item) -> Translates:
        ...

    def __getitem__(self, item: Union[str, int]):
        return self.__getattr__(item)


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
                raise TranslateKeyNotFound
                # raise TranslateKeyNotFound(f'there\'s no key {item} in both {DR_option.language} and zh-CN')

    def lang(self, *args) -> Union[int, str, list, dict, tuple]:
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
                raise TranslateKeyNotFound from e
                # raise TranslateKeyNotFound(f'there\'s no key {args} in both {DR_option.language} and zh-CN') from e

    def 翻译(self, *args) -> Union[int, str, list, dict]:
        return self.lang(args)

    def _update_lang(self) -> str:
        """
        用于更新语言(内部调用)
        :return: 设置完成后的语言
        """
        self.translates = tools.load_file(f'configs/lang/{DR_option.language}.toml')
        return DR_option.language


if __name__ == '__main__':
    tr_ = Tr()
else:
    tr = Lang()
