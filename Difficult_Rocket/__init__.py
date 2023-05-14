#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import sys
import time
import importlib
import traceback
import contextlib
import importlib.util
from pathlib import Path
from typing import Optional, List, Tuple

from Difficult_Rocket.api.types import Options
from Difficult_Rocket.utils.thread import new_thread

from libs.MCDR.version import Version

game_version = Version("0.7.2.2")  # 游戏版本
build_version = Version("1.2.1.0")  # 编译文件版本(与游戏本体无关)
Api_version = Version("0.1.0.0")  # API 版本
__version__ = game_version

long_version: int = 15
"""
long_version: 一个用于标记内部协议的整数
15: 完全移除 DR_rust 相关内容 解耦完成
14: BaseScreen 的每一个函数都添加了一个参数: window: "ClientWindow"
13: 为 DR_runtime 添加 API_version
12: 去除 DR_runtime 的 global_logger
    要 logging 自己拿去（
11: 为 DR_option  添加 use_DR_rust
    修复了一些拼写错误
10: 为 DR_runtime 添加 DR_Rust_get_version
9 : 为 DR_option  添加 pyglet_macosx_dev_test
8 : 为 DR_runtime 添加 DR_rust_version
    为 DR_option  添加 DR_rust_available
    以后就有 DR_rust 了
7 : 为 DR_option 添加 std_font_size
6 : 事实证明, 不如直接用int
5 : 添加 build_version 信息,用于标记编译文件版本,
    游戏版本改为四位数，终于有一个可以让我随便刷的版本号位数了
4 : 把 translate 的字体常量位置改了一下,顺便调换顺序
3 : 就是试试改一下，正好 compiler 要用
2 : 哦，对 longlong 好耶！
1 : 我可算想起来还有这回事了 v0.6.4
"""


class _DR_option(Options):
    """
    DR 的一般配置/状态
    """
    name = 'DR Option'
    # runtime options
    InputBox_use_TextEntry:     bool = True
    record_threads:             bool = True
    report_translate_not_found: bool = True
    use_multiprocess:           bool = False
    DR_rust_available:          bool = False
    use_cProfile:               bool = False
    use_local_logging:          bool = False
    
    # tests
    playing:                bool = False
    debugging:              bool = False
    crash_report_test:      bool = False

    # window option
    gui_scale: float = 1.0  # default 1.0 2.0 -> 2x 3 -> 3x

    @property
    def std_font_size(self) -> int:
        return round(12 * self.gui_scale)


class _DR_runtime(Options):
    """
    DR 的运行时配置/状态
    """
    name = 'DR Runtime'
    # game version status
    DR_version: Version = game_version  # DR SDK 版本
    Build_version: Version = build_version  # DR 构建 版本

    API_version: Version = Api_version  # DR SDK API 版本
    DR_long_version: int = long_version  # DR SDK 内部协议版本 （不要问我为什么不用 Version，我也在考虑）

    DR_Mod_List: List[Tuple[str, Version]] = []  # DR Mod 列表 (name, version)
    
    # run status
    running:               bool = False
    start_time_ns:         Optional[int] = None
    client_setup_cause_ns: Optional[int] = None
    server_setup_cause_ns: Optional[int] = None

    # game runtimes
    # global_logger: logging.Logger

    # game options
    mod_path: str = './mods'
    language: str = 'zh-CN'
    default_language: str = 'zh-CN'

    def load_file(self) -> bool:
        with contextlib.suppress(FileNotFoundError):
            with open('./configs/main.toml', 'r', encoding='utf-8') as f:
                import rtoml
                config_file = rtoml.load(f)
                self.language = config_file['runtime']['language']
                self.mod_path = config_file['game']['mods']['path']
                return True
        return False

    def find_mods(self) -> List[str]:
        mods = []
        mod_path = Path(self.mod_path)
        if not mod_path.exists():
            mod_path.mkdir()
            return []
        paths = mod_path.iterdir()
        sys.path.append(self.mod_path)
        for mod_path in paths:
            try:
                if mod_path.is_dir() and mod_path.name != '__pycache__':  # 处理文件夹 mod
                    if importlib.util.find_spec(mod_path.name) is not None:
                        mods.append(mod_path.name)
                    else:
                        print(f'can not import mod {mod_path} because importlib can not find spec')
                elif mod_path.suffix in ('.pyz', '.zip'):  # 处理压缩包 mod
                    if importlib.util.find_spec(mod_path.name) is not None:
                        mods.append(mod_path.name)
                elif mod_path.suffix == '.pyd':  # pyd 扩展 mod
                    if importlib.util.find_spec(mod_path.name) is not None:
                        mods.append(mod_path.name)
                elif mod_path.suffix == '.py':  # 处理单文件 mod
                    print(f'importing mod {mod_path=} {mod_path.stem}')
                    if importlib.util.find_spec(mod_path.stem) is not None:
                        mods.append(mod_path.stem)
            except ImportError:
                print(f'ImportError when loading mod {mod_path}')
                traceback.print_exc()
        return mods


DR_option = _DR_option()
DR_runtime = _DR_runtime()

if DR_option.playing:
    def think_it(something):
        return something


    @new_thread('think')
    def think(some_thing_to_think):
        gotcha = think_it(some_thing_to_think)
        return gotcha
