"""
@author shenjackyuanjie
@contact 3695888@qq.com
"""
import atexit
import logging
import threading

from typing import Optional, Union
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, FATAL

from Difficult_Rocket.utils.thread import ThreadLock

color_reset_suffix = "\033[0m"

"""
logging.py
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
"""

DETAIL = 5



class LogFileCache:
    """日志文件缓存"""

    def __init__(self, file_name: str = 'logs//log.log', flush_time: Optional[Union[int, float]] = 1, log_cache_lens_max: int = 10):
        """

        @param file_name: 日志文件名称
        @param flush_time: 刷新日志缓存，写入文件的时长间隔
        @param log_cache_lens_max: 日志缓存在自动写入前的最大缓存长度
        """
        # 配置相关
        self._logfile_name = file_name  # log 文件名称
        self.flush_time = flush_time  # 缓存刷新时长
        self.cache_entries_num = log_cache_lens_max
        # 写入缓存数
        self.cache_count = 0
        # 日志缓存表
        self.logs_cache = []
        # 同步锁
        self.thread_lock = threading.Lock()
        self.with_thread_lock = ThreadLock(self.thread_lock)
        self.threaded_write = threading.Timer(1, self._log_file_time_write)

    def end_thread(self):
        """结束日志写入进程，顺手把目前的缓存写入"""
        self.thread_lock.acquire(blocking=True)
        self.threaded_write.cancel()
        if self.cache_count:
            self._log_file_time_write()

    def start_thread(self):
        self.threaded_write.start()
        atexit.register(self.end_thread)

    @property
    def logfile_name(self) -> str:
        return self._logfile_name

    @logfile_name.setter
    def logfile_name(self, value: str) -> None:
        with self.with_thread_lock:
            self._logfile_name = value

    def _log_file_time_write(self) -> None:
        """使用 threading.Timer 调用的定时写入日志文件的函数"""
        with self.with_thread_lock:
            if self.cache_count == 0:
                return None
        ...

    def write_logs(self, string: str, wait_for_cache: bool = True) -> None:
        if wait_for_cache:
            with open(file=self.logfile_name, encoding='utf-8', mode='a') as log_file:
                log_file.writelines(self.logs_cache)
                log_file.write(string)
            ...
        else:
            ...


class Logger:
    """shenjack logger"""

    def __init__(self, config: dict = None, **kwargs) -> None:
        """请注意，如果需要获取一个"""
        self.name = 'root'
        if config is None:
            if name := kwargs.pop('name', default=False):
                self.name = name
        else:
            ...

    def make_log(self, level: int,
                 *values: object,
                 sep: Optional[str] = ' ',
                 end: Optional[str] = '\n',
                 flush: Optional[bool] = False) -> None:
        ...

    def detail(self, *values: object,
               sep: Optional[str] = ' ',
               end: Optional[str] = '\n',
               flush: Optional[bool] = False) -> None:
        self.make_log(level=DETAIL, *values, sep=sep, end=end, flush=flush)

    def debug(self,
              *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False) -> None:
        self.make_log(level=DEBUG, *values, sep=sep, end=end, flush=flush)

    def info(self,
             *values: object,
             sep: Optional[str] = ' ',
             end: Optional[str] = '\n',
             flush: Optional[bool] = False) -> None:
        self.make_log(level=INFO, *values, sep=sep, end=end, flush=flush)

    def warning(self,
                *values: object,
                sep: Optional[str] = ' ',
                end: Optional[str] = '\n',
                flush: Optional[bool] = False) -> None:
        self.make_log(level=WARNING, *values, sep=sep, end=end, flush=flush)

    def error(self,
              *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False) -> None:
        self.make_log(level=ERROR, *values, sep=sep, end=end, flush=flush)

    def fatal(self,
              *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False) -> None:
        self.make_log(level=FATAL, *values, sep=sep, end=end, flush=flush)


logger_configs = {
    'root': {
        'level': DEBUG,
        'color': {
            DEBUG: '\033[0m'
        },
        'file': {
            'mode': 'a',
            'encoding': 'utf-8'
        },
        ...: ...
    }
}


def add_dict_config_to_global(some_dict: dict, name: str) -> dict:
    """

    @param some_dict: 一个你丢进来的 logger 设置
    @param name: 这个 logger 设置的名称
    @return: 修改过的 logger 配置
    """
    logger_configs[name] = some_dict
    return logger_configs


def add_kwargs_to_global(**kwargs) -> dict:
    """

    @param kwargs:
    @return:
    """
    ...

