#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import time
# import logging.config
from pathlib import Path

from Difficult_Rocket.api.types import Options, Version

sdk_version = Version("0.8.7.3")  # SDK 版本
build_version = Version("2.2.0.0")  # 编译文件版本(与游戏本体无关)
api_version = Version("0.1.1.0")  # API 版本
__version__ = sdk_version


__all__ = [
    # __init__
    "DR_status",
    # folder
    "api",
    "data",
    "client",
    "command",
    "crash",
    "exception",
    "server",
    "mod",
    "utils",
    # file
    "main",
    "runtime",
    "sdk_version",
    "build_version",
    "api_version",
]


class _DRStatus(Options):
    """
    DR 的特性开关 / 基本状态
    """

    name = "DR Option"
    # run status
    client_running: bool = False
    server_running: bool = False

    # feature switch
    InputBox_use_TextEntry: bool = True
    record_threads: bool = True
    report_translate_not_found: bool = True
    use_multiprocess: bool = False
    use_cProfile: bool = False
    use_local_logging: bool = False

    # tests
    playing: bool = False
    debugging: bool = False
    crash_report_test: bool = False

    # game version status
    DR_version: Version = sdk_version  # DR SDK 版本
    Build_version: Version = build_version  # DR 构建 版本
    API_version: Version = api_version  # DR SDK API 版本

    # game options
    default_language: str = "zh-CN"

    # window option
    gui_scale: float = 1.0  # default 1.0 2.0 -> 2x 3 -> 3x

    @property
    def std_font_size(self) -> int:
        return round(12 * self.gui_scale)


DR_status = _DRStatus()


def load_logging():
    # with open("./config/logger.toml") as f:
    #     import rtoml
    #
    #     logger_config = rtoml.load(f)
    # log_path = logger_config["handlers"]["file"]["filename"]
    # log_path = f"logs/{log_path.format(time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime(time.time_ns() / 1000_000_000)))}"
    # if not Path("logs/").is_dir():
    #     Path("logs/").mkdir()
    # logger_config["handlers"]["file"]["filename"] = log_path
    # logging.config.dictConfig(logger_config)
    log_config_path = Path("./config/lndl-logger.toml")

    import rtoml

    if not log_config_path.is_file():
        # 生成默认配置文件
        from Difficult_Rocket.data import log_config
        log_config_path.write_text(log_config.default_config)
        logger_config = rtoml.loads(log_config.default_config)
    else:
        # 读取配置文件
        with open(log_config_path, encoding='utf-8') as f:
            logger_config = rtoml.load(f)
    # 输入 lndl 进行配置
    from lib_not_dr.loggers.config import read_config
    read_config(logger_config)


load_logging()


if DR_status.playing:
    from Difficult_Rocket.utils.thread import new_thread

    def think_it(something):
        return something

    @new_thread("think")
    def think(some_thing_to_think):
        gotcha = think_it(some_thing_to_think)
        return gotcha
