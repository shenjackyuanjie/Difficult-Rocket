#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import sys
import importlib
import traceback
import contextlib
import importlib.util
from pathlib import Path
from typing import Optional, List, Tuple

from Difficult_Rocket.api.types import Options, Version

game_version = Version("0.8.2.0")  # 游戏版本
build_version = Version("2.1.0.0")  # 编译文件版本(与游戏本体无关)
Api_version = Version("0.1.1.0")  # API 版本
__version__ = game_version


class _DR_status(Options):
    """
    DR 的特性开关 / 基本状态
    """
    name = 'DR Option'
    # run status
    client_running: bool = False
    server_running: bool = False

    # feature switch
    InputBox_use_TextEntry:     bool = True
    record_threads:             bool = True
    report_translate_not_found: bool = True
    use_multiprocess:           bool = False
    use_cProfile:               bool = False
    use_local_logging:          bool = False
    
    # tests
    playing:                bool = False
    debugging:              bool = False
    crash_report_test:      bool = False

    # game version status
    DR_version: Version = game_version  # DR SDK 版本
    Build_version: Version = build_version  # DR 构建 版本
    API_version: Version = Api_version  # DR SDK API 版本

    # game options
    default_language: str = 'zh-CN'

    # window option
    gui_scale: float = 1.0  # default 1.0 2.0 -> 2x 3 -> 3x

    @property
    def std_font_size(self) -> int:
        return round(12 * self.gui_scale)


class _DR_runtime(Options):
    """
    DR 的运行时配置 / 状态
    """
    name = 'DR Runtime'

    language: str = 'zh-CN'
    mod_path: str = './mods'
    DR_Mod_List: List[Tuple[str, Version]] = []  # DR Mod 列表 (name, version)
    
    # run status
    start_time_ns:         Optional[int] = None
    client_setup_cause_ns: Optional[int] = None
    server_setup_cause_ns: Optional[int] = None

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


DR_status = _DR_status()
DR_runtime = _DR_runtime()

if DR_status.playing:
    from Difficult_Rocket.utils.thread import new_thread

    def think_it(something):
        return something


    @new_thread('think')
    def think(some_thing_to_think):
        gotcha = think_it(some_thing_to_think)
        return gotcha
