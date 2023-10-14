#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import shutil
import traceback
from io import StringIO
from typing import get_type_hints, Type, List, Union, Dict, Any, Callable, Tuple, Optional, TYPE_CHECKING, Iterable

__all__ = [
    'get_type_hints_',
    'Options',
    'OptionsError',
    'OptionNotFound',
    'OptionNameNotDefined'
]


def get_type_hints_(cls: Type):
    try:
        return get_type_hints(cls)
    except ValueError:
        return get_type_hints(cls, globalns={})


def to_str_value_(value: Any) -> Any:
    """递归的将输入值的每一个非 builtin type 转换成 str"""
    if isinstance(value, (str, bytes, bytearray, int, float, bool, type(None))):
        return value
    elif isinstance(value, dict):
        return {k: to_str_value_(v) for k, v in value.items()}
    elif isinstance(value, (list, Iterable)):
        return [to_str_value_(v) for v in value]
    else:
        return str(value)


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
    存储配置: 继承 Options 类
            在类里定义 option: typing
            (可选 定义 name: str = 'Option Base' 用于在打印的时候显示名字)
    提供 API 接口: 继承 Options 类
            在类里定义 option: typing
            定义 一些需要的方法
            子类: 继承 新的 Options 类
                实现定义的方法
    """
    name = 'Option Base'
    cached_options: Dict[str, Union[str, Any]] = {}
    _check_options: bool = True

    def __init__(self, **kwargs):
        """
        创建一个新的 Options 的时候的配置
        如果存在 init 方法 会在设置完 kwargs 之后运行子类的 init 方法
        :param kwargs: 需要设置的选项
        """
        if TYPE_CHECKING:
            self._options: Dict[str, Union[Callable, object]] = {}
        self.flush_option()
        for option, value in kwargs.items():
            if option not in self.cached_options and self._check_options:
                raise OptionNameNotDefined(f"option: {option} with value: {value} is not defined")
            setattr(self, option, value)
        run_load_file = True
        if hasattr(self, 'init'):
            run_load_file = self.init(**kwargs)  # 默认 False/None
            run_load_file = not run_load_file
        if hasattr(self, 'load_file') and run_load_file:
            try:
                self.load_file()
            except Exception:
                traceback.print_exc()
        self.flush_option()

    def __str__(self):
        return f"<{self.__class__.__name__} {self.name}>" if self.name else f"<{self.__class__.__name__}>"

    def __repr__(self):
        return self.__str__()

    if TYPE_CHECKING:
        _options: Dict[str, Union[Callable, object]] = {}

        def init(self, **kwargs) -> bool:
            """ 如果子类定义了这个函数，则会在 __init__ 之后调用这个函数
            返回值为 True 则不会调用 load_file 函数
            """

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

    def str_option(self, shrink_to_long: Optional[int] = None) -> Dict[str, Union[str, Any]]:
        """
        获取配置类的所有配置 并将所有非 BuiltIn 类型的值转换为 str
        :return:
        """
        raw_option = self.option()
        str_option = to_str_value_(raw_option)
        if shrink_to_long is None:
            return str_option
        if not isinstance(shrink_to_long, int) or shrink_to_long <= 0:
            return str_option
        for option, value in str_option.items():
            if value is not None:
                if len(str(value)) > shrink_to_long:
                    str_option[option] = str(value)[:shrink_to_long] + '...'
        return str_option

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

    def option_with_len(self) -> Tuple[List[Tuple[str, Any, Type]], int, int, int]:
        """
        返回一个可以用于打印的 option 列表
        :return:
        """
        options = self.flush_option()
        max_len_key = 1
        max_len_value = 1
        max_len_value_t = 1
        option_list = []
        for key, value in options.items():
            value_t = type(value) if isinstance(value, type(value)) else type(value)  # 判定这个类型 是不是 基本类型
            max_len_key = max(max_len_key, len(key))
            max_len_value = max(max_len_value, len(str(value)))
            max_len_value_t = max(max_len_value_t, len(str(value_t)))
            option_list.append([key, value, value_t])
        return [option_list, max_len_key, max_len_value, max_len_value_t]  # noqa

    def as_markdown(self, longest: Optional[int] = None) -> str:
        """
        返回一个 markdown 格式的 option 字符串
        :param longest: 最长的输出长度
        :return: markdown 格式的 option 字符串
        """
        value = self.option_with_len()
        cache = StringIO()
        option_len = max(value[1], len('Option'))
        value_len = max(value[2], len('Value'))
        value_type_len = max(value[3], len('Value Type'))

        # | Option | Value | Value Type |
        shortest = len('Option | Value | Value Type')

        if longest is not None:
            console_width = max(longest, shortest)
        else:
            console_width = shutil.get_terminal_size(fallback=(100, 80)).columns
            console_width = max(console_width, shortest)

        # 为每一栏 预分配 1/3 或者 需要的宽度 (如果不需要 1/3)
        option_len = min(option_len, console_width // 3)
        value_len = min(value_len, console_width // 3)
        value_type_len = min(value_type_len, console_width // 3)

        # 先指定每一个列的输出最窄宽度, 然后去尝试增加宽度
        # 循环分配新空间之前 首先检查是否已经不需要多分配 (and 后面)
        while option_len + value_len + value_type_len + 16 < console_width\
                and (option_len < value[1]
                     or value_len < value[2]
                     or value_type_len < value[3]):
            # 每一个部分的逻辑都是
            # 如果现在的输出长度小于原始长度
            # 并且长度 + 1 之后的总长度依然在允许范围内
            # 那么就 + 1
            if option_len < value[1] and option_len + value_len + value_type_len + 16 < console_width:
                option_len += 1
            if value_len < value[2] and option_len + value_len + value_type_len + 16 < console_width:
                value_len += 1
            if value_type_len < value[3] and option_len + value_len + value_type_len + 16 < console_width:
                value_type_len += 1
        # 实际上 对于列表(可变对象) for 出来的这个值是一个引用
        # 所以可以直接修改 string
        for v in value[0]:
            if len(str(v[0])) > option_len:
                v[0] = f'{str(v[0])[:value_len - 3]}...'
            if len(str(v[1])) > value_len:
                v[1] = f'{str(v[1])[:value_len - 3]}...'
            if len(str(v[2])) > value_type_len:
                v[2] = f'{str(v[2])[:value_len - 3]}..'

        cache.write(
            f"| Option{' ' * (option_len - 3)}| Value{' ' * (value_len - 2)}| Value Type{' ' * (value_type_len - 7)}|\n")
        cache.write(f'|:{"-" * (option_len + 3)}|:{"-" * (value_len + 3)}|:{"-" * (value_type_len + 3)}|\n')
        for option, value, value_t in value[0]:
            cache.write(f"| `{option}`{' ' * (option_len - len(option))} "
                        f"| `{value}`{' ' * (value_len - len(str(value)))} "
                        f"| `{value_t}`{' ' * (value_type_len - len(str(value_t)))} |\n")
        result = cache.getvalue()
        cache.close()
        return result

    @classmethod
    def add_option(cls, name: str, value: Union[Callable, object]) -> Dict:
        """
        向配置类中添加一个额外的配置
        :param name: 配置的名字
        :param value: 用于获取配置的函数或者类
        :return: 配置类的所有配置
        """
        if not hasattr(cls, '_options'):
            cls._options: Dict[str, Union[Callable, object]] = {}
        cls._options[name] = value
        return cls._options

    @staticmethod
    def init_option(options_class: Type['Options'], init_value: Optional[dict] = None) -> 'Options':
        return options_class(**init_value if init_value is not None else {})
