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

from typing import Any, Dict, Callable, Union, Tuple, List, get_type_hints, Type

from Difficult_Rocket.utils.typings import Options

from libs.MCDR.version import Version

game_version = Version("0.6.3")
__version__ = game_version



class _DR_option(Options):
    """
    DR 的整体配置存储类
    """
    # runtime options
    InputBox_use_TextEntry: bool = False
    record_threads: bool = True
    use_cProfile: bool = False
    use_local_logging: bool = False

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
print(DR_option.option())
print(_DR_option.option())
_DR_option.use_cProfile = True
print(_DR_option.option())
# print(_DR_option.__dict__)
# print(DR_option.__dir__())
# print(_DR_option.__dir__)

if DR_option.playing:
    from Difficult_Rocket.utils import new_thread


    def think_it(something):
        return something


    @new_thread('think')
    def think(some_thing_to_think):
        gotcha = think_it(some_thing_to_think)
        return gotcha
