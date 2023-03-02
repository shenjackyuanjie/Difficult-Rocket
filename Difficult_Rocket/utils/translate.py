#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
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
from typing import Union, Tuple, Any, List, Dict, Hashable, Optional

from Difficult_Rocket import DR_runtime, DR_option
from Difficult_Rocket.utils import tools
from Difficult_Rocket.exception.language import *


@dataclass
class TranslateConfig:
    raise_error: bool = False  # 引用错误时抛出错误
    crack_normal: bool = True  # 出现错误引用后 将引用到的正确内容替换为引用路径
    insert_crack: bool = True  # 加入引用的错误内容
    is_final: bool = False  # 是否为最终内容
    keep_get: bool = True  # 引用错误后是否继续引用
    always_copy: bool = False  # 是否一直新建 Translate (为 True 会降低性能)
    source: Optional[Union["Tr", "Translates"]] = None  # 翻译来源 (用于默认翻译)

    def set(self, item: str, value: Union[bool, "Tr", "Translates"]) -> 'TranslateConfig':
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
                               always_copy=self.always_copy,
                               source=self.source)

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
        elif DR_option.report_translate_not_found:
            frame = inspect.currentframe()
            if frame is not None:
                frame = frame.f_back.f_back
                code_list = [self.__getitem__.__code__, self.__getattr__.__code__,
                             self.__copy__.__code__, self.copy.__code__,
                             Tr.lang.__code__, Tr.__getitem__.__code__,
                             Tr.__call__.__code__]  # 调用堆栈上的不需要的东西
                while True:
                    if frame.f_code not in code_list:  # 直到调用堆栈不是不需要的东西
                        break
                    frame = frame.f_back  # 继续向上寻找
                frame = f'call at {frame.f_code.co_filename}:{frame.f_lineno}'
            else:
                frame = 'but No Frame environment'
            raise_info = f"{self.name} Cause a error when getting {item} {frame}"
            print(raise_info)

    def __getitem__(self, item: Union[key_type, List[key_type], Tuple[key_type]]) -> "Translates":
        try:
            if isinstance(item, (str, int, Hashable)):
                cache_value = self.value[item]
            else:
                cache_value = self.value
                for a_item in item:
                    cache_value = cache_value[a_item]
            if isinstance(cache_value, (int, str,)):
                self.config.is_final = True
            self.get_list.append((True, item))
            if self.config.always_copy:
                return Translates(value=cache_value, config=self.config, get_list=self.get_list)
            self.value = cache_value
        except (KeyError, TypeError, AttributeError) as e:
            self.get_list.append((False, item))
            self._raise_no_value(e, item)
            if not self.config.keep_get:
                self.config.is_final = True
        return self

    def __call__(self, *args, **kwargs) -> Union[dict, list, int, str]:
        return self.__str__()

    def copy(self):
        return self.__copy__()

    def __copy__(self) -> 'Translates':
        return Translates(value=self.value, config=self.config, get_list=self.get_list)

    def __getattr__(self, item: key_type) -> "Translates":
        if (self.config.is_final or any(x[0] for x in self.get_list)) and hasattr(self.value, item):
            return getattr(self.value, item)
        # 实际上我这里完全不需要处理正常需求，因为 __getattribute__ 已经帮我处理过了
        return self.__getitem__(item)

    def __str__(self):
        if not any(not x[0] for x in self.get_list):
            return self.value
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
        self.language_name = language if language is not None else DR_runtime.language
        self.translates: Dict[str, Union[str, Dict]] = tools.load_file(f'configs/lang/{self.language_name}.toml')
        self.default_translate: Dict = tools.load_file(f'configs/lang/{DR_runtime.default_language}.toml')
        self.default_config = config.set('source', self) if config is not None else TranslateConfig(source=self)
        self.translates_cache = Translates(value=self.translates, config=self.default_config.copy())

    def init_translate(self):
        self.translates: Dict[str, Union[str, Dict]] = tools.load_file(f'configs/lang/{self.language_name}.toml')
        self.default_translate: Dict = tools.load_file(f'configs/lang/{DR_runtime.default_language}.toml')
        self.translates_cache = Translates(value=self.translates, config=self.default_config.copy())

    def update_lang(self) -> bool:
        if DR_runtime.language != self.language_name:
            self.language_name = DR_runtime.language
            self.init_translate()
            return True
        return False

    def default(self, items: Union[str, List[str]]) -> Translates:
        if isinstance(items, list):
            cache_translate = self.default_translate
            for item in items:
                cache_translate = cache_translate[item]
            return cache_translate
        else:
            return self.default_translate[items]

    def lang(self, *items) -> Translates:
        cache = self.translates_cache.copy()
        for item in items:
            cache = cache[item]
        return cache

    def __getitem__(self, item: Union[str, int]) -> Translates:
        return self.translates_cache.copy()[item]

    def __call__(self, *args, **kwargs) -> Translates:
        return self.translates_cache.copy()


tr = Tr()
