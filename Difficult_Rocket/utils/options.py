#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import traceback
from io import StringIO
from dataclasses import dataclass
from typing import get_type_hints, Type, List, Union, Dict, Any, Callable, Tuple, Optional, TYPE_CHECKING

__all__ = ['get_type_hints_',
           'Options',
           'Fonts',
           'FontData',
           'OptionsError',
           'OptionNotFound',
           'OptionNameNotDefined']


def get_type_hints_(cls: Type):
    try:
        return get_type_hints(cls)
    except ValueError:
        return get_type_hints(cls, globalns={})


class OptionsError(Exception):
    """ option 的错误基类"""


class OptionNameNotDefined(OptionsError):
    """ 向初始化的 option 里添加了一个不存在于选项里的选项 """


class OptionNotFound(OptionsError):
    """ 某个选项没有找到 """


class Options:
    """
    一个用于存储选项 / 提供 API 定义 的类
    用法:
    继承 Options 类
    在类里定义 option: typing
    (可选 定义 name: str = 'Option Base' 用于在打印的时候显示名字)
    
    """
    name = 'Option Base'
    cached_options: Dict[str, Union[str, Any]] = {}

    def __init__(self, **kwargs):
        """
        创建一个新的 Options 的时候的配置
        如果存在 init 方法 会在设置完 kwargs 之后运行子类的 init 方法
        :param kwargs:
        """
        if TYPE_CHECKING:
            self._options: Dict[str, Union[Callable, object]] = {}
        self.flush_option()
        for option, value in kwargs.items():
            if option not in self.cached_options:
                raise OptionNameNotDefined(f"option: {option} with value: {value} is not defined")
            setattr(self, option, value)
        if hasattr(self, 'init'):
            self.init(**kwargs)
        if hasattr(self, 'load_file'):
            try:
                self.load_file()
            except Exception:
                traceback.print_exc()
        self.flush_option()

    if TYPE_CHECKING:
        _options: Dict[str, Union[Callable, object]] = {}

        def init(self, **kwargs) -> None:
            """ 如果子类定义了这个函数，则会在 __init__ 之后调用这个函数 """

        def load_file(self) -> bool:
            """如果子类定义了这个函数，则会在 __init__ 和 init 之后再调用这个函数

            请注意，这个函数请尽量使用 try 包裹住可能出现错误的部分
            否则会在控制台输出你的报错"""
            return True

    def option(self) -> Dict[str, Any]:
        """
        获取配置类的所有配置
        :return: 自己的所有配置
        """
        values = {}
        for ann in self.__annotations__:  # 获取类型注释
            values[ann] = getattr(self, ann, None)
            if values[ann] is None:
                values[ann] = self.__annotations__[ann]

        if not hasattr(self, '_options'):
            self._options: Dict[str, Union[Callable, object]] = {}
        for option, a_fun in self._options.items():  # 获取额外内容
            values[option] = a_fun

        for option, a_fun in values.items():  # 检查是否为 property
            if a_fun is bool and getattr(self, option, None) is not None:
                values[option] = False
            if isinstance(a_fun, property):
                try:
                    values[option] = getattr(self, option)
                except AttributeError:
                    raise OptionNotFound(f'Option {option} is not found in {self.name}') from None
        return values

    def format(self, text: str) -> str:
        """
        使用自己的选项给输入的字符串替换内容
        :param text: 想替换的内容
        :return: 替换之后的内容
        """
        cache_option = self.flush_option()
        for option, value in cache_option.items():
            text = text.replace(f'{{{option}}}', str(value))
        return text

    def flush_option(self) -> Dict[str, Any]:
        """
        刷新缓存 options 的内容
        :return: 刷新过的 options
        """
        self.cached_options = self.option()
        return self.cached_options

    def option_with_len(self) -> Tuple[List[Tuple[str, Union[Any, Type], Type]], int, int, int]:
        options = self.flush_option()
        max_len_key = 1
        max_len_value = 1
        max_len_value_t = 1
        option_list = []
        for key, value in options.items():
            value_t = value if isinstance(value, Type) else type(value)  # 判定这个类型 是不是 基本类型
            max_len_key = max(max_len_key, len(key))
            max_len_value = max(max_len_value, len(str(value)))
            max_len_value_t = max(max_len_value_t, len(str(value_t)))
            option_list.append((key, value, value_t))
        return option_list, max_len_key, max_len_value, max_len_value_t

    def as_markdown(self) -> str:
        value = self.option_with_len()
        cache = StringIO()
        option_len = max(value[1], len('Option'))
        value_len = max(value[2], len('Value'))
        value_type_len = max(value[3], len('Value Type'))
        cache.write(f"| Option{' '*(option_len-3)}| Value{' '*(value_len-2)}| Value Type{' '*(value_type_len-7)}|\n")
        cache.write(f'|:{"-" * (option_len+3)}|:{"-" * (value_len+3)}|:{"-" * (value_type_len + 3)}|\n')
        for option, value, value_t in value[0]:
            cache.write(f"| `{option}`{' '* (option_len - len(option))} "
                        f"| `{value}`{' '* (value_len - len(str(value)))} "
                        f"| `{value_t}`{' '* (value_type_len - len(str(value_t)))} |\n")
        result = cache.getvalue()
        cache.close()
        return result

    @classmethod
    def add_option(cls, name: str, value: Union[Callable, object]) -> Dict:
        if not hasattr(cls, '_options'):
            cls._options: Dict[str, Union[Callable, object]] = {}
        cls._options[name] = value
        return cls._options

    @staticmethod
    def init_option(options_class: Type['Options'], init_value: Optional[dict] = None) -> 'Options':
        return options_class(**init_value if init_value is not None else {})


class Fonts(Options):
    # font's value

    HOS: str = 'HarmonyOS Sans'
    HOS_S: str = 'HarmonyOS Sans SC'
    HOS_T: str = 'HarmonyOS Sans TC'
    HOS_C: str = 'HarmonyOS Sans Condensed'

    鸿蒙字体: str = HOS
    鸿蒙简体: str = HOS_S
    鸿蒙繁体: str = HOS_T
    鸿蒙窄体: str = HOS_C

    CC: str = 'Cascadia Code'
    CM: str = 'Cascadia Mono'
    CCPL: str = 'Cascadia Code PL'
    CMPL: str = 'Cascadia Mono PL'

    微软等宽: str = CC
    微软等宽无线: str = CM
    微软等宽带电线: str = CCPL
    微软等宽带电线无线: str = CMPL

    得意黑: str = '得意黑'
    # SS = smiley-sans
    SS: str = 得意黑


@dataclass
class FontData:
    """ 用于保存字体的信息 """
    font_name: str = Fonts.鸿蒙简体
    font_size: int = 13
    bold: bool = False
    italic: bool = False
    stretch: bool = False

    def dict(self) -> Dict[str, Union[str, int, bool]]:
        return dict(font_name=self.font_name,
                    font_size=self.font_size,
                    bold=self.bold,
                    italic=self.italic,
                    stretch=self.stretch)
