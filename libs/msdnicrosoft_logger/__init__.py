from time import strftime

__all__ = [
    "Log"
]


class Log:
    """
    参数:\n
    Shell -- 是否输出消息 -> 控制台 (Default：True) | Boolean\n
    LogFile -- 是否输出消息 -> 文件 (Default: False) | Boolean\n
    FileName [已使用格式化时间] -- 输出文件名（仅 LogFile=True 时此参数有效）（Default：%Y-%m-%d_%H-%M.log） | String\n
    FileName 请注意符合对应操作系统的文件命名要求\n
    """

    def __init__(self,
                 Shell=True,
                 LogFile=False,
                 FileName="%Y-%m-%d_%H-%M.log"
                 ):
        self.Shell = Shell
        self.LogFile = LogFile
        self.FileName = FileName

    def info(self, Message):
        if self.Shell:
            Console.info(Message)
        if self.LogFile:
            file = File(FileName=self.FileName)
            file.info(Message)

    def warning(self, Message):
        if self.Shell:
            Console.warning(Message)
        if self.LogFile:
            file = File(FileName=self.FileName)
            file.warning(Message)

    def error(self, Message):
        if self.Shell:
            Console.error(Message)
        if self.LogFile:
            file = File(FileName=self.FileName)
            file.error(Message)

    def fatal(self, Message):
        if self.Shell:
            Console.fatal(Message)
        if self.LogFile:
            file = File(FileName=self.FileName)
            file.fatal(Message)

    def debug(self, Message):
        if self.Shell:
            Console.debug(Message)
        if self.LogFile:
            file = File(FileName=self.FileName)
            file.debug(Message)


class Console:
    """
    This class can output colored messages to Shell.
    """
    from colorama import init
    sColorSuffix = "\033[0m"
    init(autoreset=True)

    @staticmethod
    def info(Message):
        print(
            strftime(
                f"[%H:%M:%S] [\033[32mINFO{Console.sColorSuffix}]: {Message}"
            )
        )

    @staticmethod
    def warning(Message):
        print(
            strftime(
                f"[%H:%M:%S] [\033[33mWARN{Console.sColorSuffix}]: {Message}"
            )
        )

    @staticmethod
    def error(Message):
        print(
            strftime(
                f"[%H:%M:%S] [\033[31mERROR{Console.sColorSuffix}]: {Message}"
            )
        )

    @staticmethod
    def fatal(Message):
        print(
            strftime(
                f"[%H:%M:%S] [\033[1;31;47mFATAL{Console.sColorSuffix}]: {Message}"
            )
        )

    @staticmethod
    def debug(Message):
        print(
            strftime(
                f"[%H:%M:%S] [\033[34mDEBUG{Console.sColorSuffix}]: {Message}"
            )
        )


class File:
    """
    This class can output messages to file.
    """

    def __init__(self, FileName):
        self.File = open(strftime(FileName), "a", encoding="utf-8")

    def __del__(self):
        self.File.close()

    def info(self, Message):
        self.File.write(
            strftime(
                f"[%H:%M:%S] [INFO]: {Message}\n"
            )
        )

    def warning(self, Message):
        self.File.write(
            strftime(
                f"[%H:%M:%S] [WARN]: {Message}\n"
            )
        )

    def error(self, Message):
        self.File.write(
            strftime(
                f"[%H:%M:%S] [ERROR]: {Message}\n"
            )
        )

    def fatal(self, Message):
        self.File.write(
            strftime(
                f"[%H:%M:%S] [FATAL]: {Message}\n"
            )
        )

    def debug(self, Message):
        self.File.write(
            strftime(
                f"[%H:%M:%S] [DEBUG]: {Message}\n"
            )
        )

import atexit

from typing import Optional

color_reset_suffix = "\033[0m"


class LogFileCache:
    """日志文件缓存"""
    def __init__(self, time_cache: Optional[int, float] = 1, log_cache: int = 10):
        self.time_cache = time_cache
        self.log_cache = log_cache


class Logger:
    """shenjack logger"""

    def __init__(self, config: dict = None) -> None:
        if config is None:
            self.config = {}
        else:
            self.config = config


class GetLogger:
    """shenjack牌logger"""

    def __init__(self):
        self.configs = {}

    def add_config(self, name: str, config: dict) -> dict:
        self.configs[name] = config
        return self.configs

    def logger(self, name: str = 'root') -> Logger:
        return Logger(config=self.configs)


if __name__ == '__main__':
    from time import sleep

    logger = Log(LogFile=True)
    logger.info("这是一条正常消息")
    sleep(1)
    logger.warning("这是一条警告消息")
    sleep(2)
    logger.error("这是一条错误消息")
    sleep(3)
    logger.fatal("这是一条致命错误消息")
    sleep(4)
    logger.debug("这是一条调试消息")
