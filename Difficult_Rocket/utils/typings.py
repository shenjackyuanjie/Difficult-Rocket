#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from typing import get_type_hints, Type, List, Union, Dict, Any, Callable, Tuple


def get_type_hints_(cls: Type):
    try:
        return get_type_hints(cls)
    except ValueError:
        return get_type_hints(cls, globalns={})


class OptionNameNotDefined(Exception):
    """向初始化的 option 里添加了一个不存在于选项里的选项"""


class Options:
    """
    Difficult Rocket 的游戏配置的存储基类
    """
    __options: Dict[str, Union[Callable, object]] = {}
    cached_options: Dict[str, Union[str, Any]] = {}

    def __init__(self, **kwargs):
        for option, value in kwargs.items():
            if option not in self.option():
                raise OptionNameNotDefined(f"option: {option} with value: {value} is not defined")
            setattr(self, option, value)
        self.flush_option()

    @classmethod
    def option(cls) -> Dict[str, Any]:
        """
        获取配置类的所有配置
        :return: 自己的所有配置
        """
        values = {}
        for ann in cls.__annotations__:  # 获取类型注释
            values[ann] = getattr(cls, ann, None)
            if values[ann] is None:
                values[ann] = cls.__annotations__[ann]

        for option, a_fun in cls.__options.items():  # 获取额外内容
            values[option] = a_fun

        for option, a_fun in values.items():  # 检查是否为 property
            if a_fun is bool and getattr(cls, option, None) is not None:
                values[option] = False
            if isinstance(a_fun, property):
                values[option] = getattr(cls, option)
        return values

    @classmethod
    def flush_option(cls) -> Dict[str, Any]:
        """
        刷新缓存 options 的内容
        :return: 刷新过的 options
        """
        cls.cached_options = cls.option()
        return cls.cached_options

    @classmethod
    def option_with_len(cls) -> List[Union[List[Tuple[str, Any, Any]], int, Any]]:
        options = cls.flush_option()
        max_len_key = 1
        max_len_value = 1
        max_len_value_t = 1
        option_list = []
        for key, value in options.items():
            value_t = type(value) if not isinstance(value, Type) else value
            max_len_key = max(max_len_key, len(key))
            max_len_value = max(max_len_value, len(str(value)))
            max_len_value_t = max(max_len_value_t, len(str(value_t)))
            option_list.append((key, value, value_t))
        return [option_list, max_len_key, max_len_value, max_len_value_t]

    @classmethod
    def add_option(cls, name, value: Union[Callable, object]) -> Dict:
        cls.__options[name] = value
        return cls.__options
