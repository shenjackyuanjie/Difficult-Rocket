#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from pathlib import Path

from Difficult_Rocket.api.types import Options, Version

sdk_version = Version("0.9.0.1")  # SDK 版本
build_version = Version("3.0.0.0")  # 编译文件版本(与游戏本体无关)
api_version = Version("0.1.2.1")  # API 版本
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

    name = "DR Status"
    # run status
    client_running: bool = False
    server_running: bool = False

    # feature switch
    InputBox_use_TextEntry: bool = True
    record_threads: bool = True
    report_translate_not_found: bool = True
    use_multiprocess: bool = False
    use_cProfile: bool = False

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


def load_logger():
    log_config_path = Path("./config/lndl-logger.toml")

    import tomli

    warn_config = False
    if not log_config_path.is_file():
        # 生成默认配置文件
        from Difficult_Rocket.data import log_config

        try:
            log_config_path.write_text(log_config.default_config)
        except (FileNotFoundError, OSError, PermissionError):
            print("\033[31mFailed to write default log config file\033[0m")
        warn_config = True
        logger_config = tomli.loads(log_config.default_config)
    else:
        # 读取配置文件
        with open(log_config_path, "rb") as f:
            logger_config = tomli.load(f)
    # 输入 lndl 进行配置
    from lib_not_dr.loggers.config import read_config, get_logger

    read_config(logger_config)
    logger = get_logger("main")
    logger.info("Logger config loaded", tag="DR-init")
    logger.info(f"DR status:\n{DR_status.as_markdown()}", tag="DR-init")
    if warn_config:
        logger.warn("Failed to load log config file, use default config", tag="DR-init")


# 读取日志配置
# 也保证可以直接运行，不带日志 ( 因为有默认配置 )
load_logger()

if DR_status.playing:
    from Difficult_Rocket.utils.thread import new_thread

    def think_it(something):
        return something

    @new_thread("think")
    def think(some_thing_to_think):
        gotcha = think_it(some_thing_to_think)
        return gotcha
