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



class LogFileCache:
    """日志文件缓存"""

    def __init__(self, file_name: str = 'logs//log.log', flush_time: Optional[Union[int, float]] = 1, cache_entries_num: int = 10):
        # 配置相关
        self._logfile_name = file_name  # log 文件名称
        self.flush_time = flush_time  # 缓存刷新时长
        self.cache_entries_num = cache_entries_num
        # 写入缓存数
        self.cache_count = 0
        # 日志缓存表
        self.logs_cache = []
        # 同步锁
        self.thread_lock = threading.Lock()
        self.with_thread_lock = ThreadLock(self.thread_lock)
        self.threaded_write = threading.Timer(1, self._log_file_time_write)

    def end_thread(self):
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
            ...
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

    def make_log(self, level: str,
                 *values: object,
                 sep: Optional[str] = ' ',
                 end: Optional[str] = '\n',
                 flush: Optional[bool] = False) -> None:
        ...

    def detail(self, *values: object,
               sep: Optional[str] = ' ',
               end: Optional[str] = '\n',
               flush: Optional[bool] = False) -> None:
        self.make_log(level='detail', *values, sep=sep, end=end, flush=flush)

    def debug(self,
              *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False) -> None:
        ...

    def info(self,
             *values: object,
             sep: Optional[str] = ' ',
             end: Optional[str] = '\n',
             flush: Optional[bool] = False) -> None:
        ...

    def warning(self,
                *values: object,
                sep: Optional[str] = ' ',
                end: Optional[str] = '\n',
                flush: Optional[bool] = False) -> None:
        ...

    def error(self,
              *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False) -> None:
        ...

    def fatal(self,
              *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False) -> None:
        ...


# class LoggerManager:
#     """shenjack牌logger"""
#
#     def __init__(self):
#         self.configs = {}
#
#     def add_config(self, name: str, config: dict) -> dict:
#         self.configs[name] = config
#         return self.configs
#
#     def get_logger(self, name: str = 'root', config: dict = None) -> Logger:
#         """相当于 logging.getLogger(name='root')"""
#         if config is not None:
#             self.add_config(name, config)
#         return Logger(config=self.configs)

global_configs = {
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
