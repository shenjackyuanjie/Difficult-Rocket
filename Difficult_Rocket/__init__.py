#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import time
import logging.config
from pathlib import Path

from Difficult_Rocket.api.types import Options, Version

game_version = Version("0.8.4.1")  # 游戏版本
build_version = Version("2.1.0.0")  # 编译文件版本(与游戏本体无关)
Api_version = Version("0.1.1.0")  # API 版本
__version__ = game_version


__all__ = [
    # __init__
    'DR_status',
    # folder
    'api',
    'client',
    'server',
    'command',
    'crash',
    'exception',
    'mod',
    'utils',
    # file
    'main',
    'runtime',
]


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


DR_status = _DR_status()


def load_logging():
    with open('./configs/logger.toml') as f:
        import rtoml
        logger_config = rtoml.load(f)
    log_path = logger_config['handlers']['file']['filename']
    log_path = f"logs/{log_path.format(time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime(time.time_ns() / 1000_000_000)))}"
    if not Path('logs/').is_dir():
        Path('logs/').mkdir()
    logger_config['handlers']['file']['filename'] = log_path
    logging.config.dictConfig(logger_config)


load_logging()


if DR_status.playing:
    from Difficult_Rocket.utils.thread import new_thread

    def think_it(something):
        return something


    @new_thread('think')
    def think(some_thing_to_think):
        gotcha = think_it(some_thing_to_think)
        return gotcha