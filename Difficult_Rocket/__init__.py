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

from typing import Any, Dict, Callable, Union

from libs.MCDR.version import Version

game_version = Version("0.6.2")
__version__ = game_version


class Options:
    """
    Difficult Rocket 的游戏配置的存储基类
    """
    _options: Dict[str, Union[Callable, object]] = {}

    def option(self) -> dict:
        values = {}
        for option, a_fun in self._options.items():
            if isinstance(a_fun, Callable):
                values[option] = a_fun()  # 例子: {'language': self.language}
            else:
                values[option] = a_fun
        return {**values, **self.__dict__}

    @classmethod
    def add_option(cls, name, value: Union[Callable, object]) -> Dict:
        cls._options[name] = value
        return cls._options


class _DR_option(Options):
    """
    DR 的整体配置存储类
    """
    # runtime options
    InputBox_use_TextEntry = False
    use_local_logging = False
    record_threads = True

    # tests
    playing = False
    debugging = False
    crash_report_test = True




class _DR_runtime(Options):
    """
    DR 的运行时配置
    """
    # run status
    start_time_ns: int = None
    client_setup_time_ns: int = None
    server_setup_time_ns: int = None

    # game options
    _language = 'zh-CN'

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


_DR_runtime.add_option('language', _DR_runtime.language)


DR_option = _DR_option()
DR_runtime = _DR_runtime()

print(_DR_runtime.__dict__)

if DR_option.playing:
    from .utils import new_thread


    def think_it(something):
        return something


    @new_thread('think')
    def think(some_thing_to_think):
        gotcha = think_it(some_thing_to_think)
        return gotcha
