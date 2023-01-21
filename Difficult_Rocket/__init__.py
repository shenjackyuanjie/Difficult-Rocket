#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""
# import ctypes
import logging
from typing import List, Dict, Union, Optional

import pyglet
from Difficult_Rocket.api.types import Options

from libs.MCDR.version import Version

game_version = Version("0.6.5.0")  # 游戏版本
build_version = Version("1.0.0.0")  # 编译文件版本(与游戏本体无关)
DR_rust_version = Version("0.0.0.1")  # DR 的 Rust 编写部分的版本
__version__ = game_version

long_version: int = 9
"""
long_version: 一个用于标记内部协议的整数
9: 为 DR_option  添加 pyglet_macosx_dev_test
8: 为 DR_runtime 添加 DR_rust_version
    为 DR_option 添加 DR_rust_available
    以后就有 DR_rust 了
7: 为 DR_option 添加 std_font_size
6: 事实证明, 不如直接用int
5: 添加 build_version 信息,用于标记编译文件版本,
   游戏版本改为四位数，终于有一个可以让我随便刷的版本号位数了
4: 把 translate 的字体常量位置改了一下,顺便调换顺序
3: 就是试试改一下，正好 compiler 要用
2: 哦，对 longlong 好耶！
1: 我可算想起来还有这回事了 v0.6.4
"""


class _DR_option(Options):
    """
    DR 的一般配置/状态
    """
    name = 'DR Option'
    # runtime options
    InputBox_use_TextEntry:    bool = True
    record_threads:            bool = True
    use_cProfile:              bool = False
    use_local_logging:         bool = False
    report_translate_no_found: bool = True
    use_muitprocess:           bool = False
    DR_rust_available:         bool = False

    # tests
    playing:                bool = False
    debugging:              bool = False
    crash_report_test:      bool = True
    pyglet_macosx_dev_test: bool = True

    # window option
    gui_scale: float = 1.0  # default 1.0 2.0 -> 2x 3 -> 3x

    def init(self, **kwargs):
        if not pyglet.compat_platform == 'darwin':  # MacOS 的测试只能在 Macos 上跑
            self.pyglet_macosx_dev_test = False
        try:
            self.DR_rust_available = True
        except ImportError:
            self.DR_rust_available = False
        self.flush_option()

    @property
    def std_font_size(self) -> int:
        return round(12 * self.gui_scale)


class _DR_runtime(Options):
    """
    DR 的运行时配置/状态
    """
    name = 'DR Runtime'
    # game status
    DR_version: Version = game_version
    Build_version: Version = build_version
    DR_Rust_version: Version = DR_rust_version
    DR_long_version: int = long_version

    # run status
    running:               bool = False
    start_time_ns:         int = None
    client_setup_cause_ns: int = None
    server_setup_cause_ns: int = None

    # game runtimes
    global_logger: logging.Logger

    # game options
    _language = 'zh-CN'
    default_language: str = 'zh-CN'

    def __init__(self, **kwargs):
        self.__options = {'language': self.language}
        super().__init__(**kwargs)

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

if DR_option.playing:
    from Difficult_Rocket.utils import new_thread


    def think_it(something):
        return something


    @new_thread('think')
    def think(some_thing_to_think):
        gotcha = think_it(some_thing_to_think)
        return gotcha
