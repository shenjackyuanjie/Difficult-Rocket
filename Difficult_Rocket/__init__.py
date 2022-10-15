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

from typing import Any, Dict, Callable, Union, Tuple, List

from libs.MCDR.version import Version

game_version = Version("0.6.3")
__version__ = game_version


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

    def option(self) -> Dict[str, Any]:
        """
        获取配置类的所有配置
        :return: 自己的所有配置
        """
        values = {}
        for ann in self.__annotations__:  # 获取类型注释
            values[ann] = getattr(self, ann, None) if getattr(self, ann, None) else self.__annotations__[ann]

        for option, a_fun in self.__options.items():  # 获取额外内容
            values[option] = a_fun

        for option, a_fun in values.items():  # 检查是否为 property
            if a_fun is bool and getattr(self, option, None) is not None:
                values[option] = False
            if isinstance(a_fun, property):
                values[option] = getattr(self, option)
        return values

    def flush_option(self) -> Dict[str, Any]:
        """
        刷新缓存 options 的内容
        :return: 刷新过的 options
        """
        self.cached_options = self.option()
        return self.cached_options

    def option_with_len(self) -> List[Union[List[Tuple[str, Any, Any]], int, Any]]:
        options = self.flush_option()
        max_len_key = 1
        max_len_value = 1
        max_len_value_t = 1
        option_list = []
        for key, value in options.items():
            value_t = type(value) if not isinstance(type(value), type(value)) else value
            # value_t = type(value) if type(value) is not type(type(value)) else value
            max_len_key = max(max_len_key, len(key))
            max_len_value = max(max_len_value, len(str(value)))
            max_len_value_t = max(max_len_value_t, len(str(value_t)))
            option_list.append((key, value, value_t))
        return [option_list, max_len_key, max_len_value, max_len_value_t]

    @classmethod
    def add_option(cls, name, value: Union[Callable, object]) -> Dict:
        cls.__options[name] = value
        return cls.__options


class _DR_option(Options):
    """
    DR 的整体配置存储类
    """
    # runtime options
    InputBox_use_TextEntry: bool = False
    use_local_logging: bool = False
    record_threads: bool = True
    use_cProfile: bool = False

    # tests
    playing: bool = False
    debugging: bool = False
    crash_report_test: bool = True


class _DR_runtime(Options):
    """
    DR 的运行时配置
    """
    # game statue
    DR_version: Version = game_version

    # run status
    start_time_ns: int = None
    client_setup_time_ns: int = None
    server_setup_time_ns: int = None

    # game options
    _language = 'zh-CN'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__options = {'language': self.language}

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value: str):
        if value == self._language:
            return
        assert isinstance(value, str), "DR language MUST be string"
        self._language = value
        from Difficult_Rocket.utils import translate
        translate.tr._update_lang()


# _DR_runtime.add_option('language', _DR_runtime.language)


DR_option = _DR_option()
DR_runtime = _DR_runtime()

if DR_option.playing:
    from .utils import new_thread


    def think_it(something):
        return something


    @new_thread('think')
    def think(some_thing_to_think):
        gotcha = think_it(some_thing_to_think)
        return gotcha
