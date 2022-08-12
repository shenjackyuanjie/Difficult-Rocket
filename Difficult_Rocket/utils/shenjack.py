"""
@author shenjackyuanjie
@contact 3695888@qq.com
"""
import os
# if __name__ == "__main__":
# os.chdir('../')

import atexit
import threading

from os import PathLike
from time import strftime
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, FATAL
from typing import Optional, Union, Dict, Iterable, Tuple, List, Callable

from Difficult_Rocket.utils.thread import ThreadLock

# 如果想要直接使用 logger 来 logging
# 直接调用 logger.debug() 即可
# 默认配置会有
# ----------
# 配置方式一
# 直接使用 logger.Logger()
# 将会创建一个空 logger
# 可以自行通过
# 配置方式二
#
#

color_reset_suffix = "\033[0m"
""" 只是用来重置颜色的后缀 """

"""
OFF > FATAL > ERROR > WARN > INFO > FINE > FINER > DEBUG > TRACE > ALL
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
ALL = NOTSET
TRACE = 5
FINE = 7

level_name_map = {
    ALL: 'ALL',  # NOTSET
    TRACE: 'TRACE',
    FINE: 'FINE',
    DEBUG: 'DEBUG',
    INFO: 'INFO',
    WARNING: 'WARNING',  # WARN
    ERROR: 'ERROR',
    FATAL: 'FATAL'
}

name_level_map = {
    'NOTSET': ALL,
    'ALL': ALL,
    'TRACE': TRACE,
    'FINE': FINE,
    'DEBUG': DEBUG,
    'INFO': INFO,
    'WARNING': WARNING,
    'WARN': WARNING,
    'ERROR': ERROR,
    'CRITICAL': FATAL,
    'FATAL': FATAL
}


class ListCache:
    """一个线程安全的列表缓存"""

    def __init__(self, lock: ThreadLock):
        self._cache = []
        self.with_thread_lock = lock

    def append(self, value: Union[str, Iterable]):
        if isinstance(value, str):
            with self.with_thread_lock:
                self._cache.append(value)
        elif isinstance(value, Iterable):
            with self.with_thread_lock:
                self._cache.append(*value)
        else:
            raise TypeError(f"cache must be string or Iterable. not a {type(value)}")

    def __getitem__(self, item):
        assert isinstance(item, int)
        with self.with_thread_lock:
            try:
                return self._cache[item]
            except IndexError as exp:
                print(f'cache:{self.cache}')
                raise IndexError(f'there is no cache at {item}!\ncache:{self.cache}')

    def __call__(self, *args, **kwargs):
        return self.cache

    def __iter__(self):
        with self.with_thread_lock:
            self._iter_cache = self._cache.copy()
            self._iter_len = len(self.cache)
        return self

    def __next__(self):
        if self._iter_cache == -1:
            raise StopIteration
        returns = self._iter_cache[-self._iter_len]
        self._iter_cache -= 1
        return returns

    def __bool__(self):
        with self.with_thread_lock:
            return True if len(self.cache) > 0 else False

    @property
    def cache(self):
        return self._cache


class LogFileCache:
    """日志文件缓存"""

    def __init__(self, file_name: PathLike = 'logs//log.log', flush_time: Optional[Union[int, float]] = 1, log_cache_lens_max: int = 10):
        """

        @param file_name: 日志文件名称
        @param flush_time: 刷新日志缓存，写入文件的时长间隔
        @param log_cache_lens_max: 日志缓存在自动写入前的最大缓存长度
        """
        # 配置相关
        self._logfile_name = file_name  # log 文件名称
        self.flush_time = flush_time  # 缓存刷新时长
        self.cache_entries_num = log_cache_lens_max
        self.started = False
        self.log
        # 同步锁
        self.cache_lock = threading.Lock()  # 主锁
        self.write_lock = threading.Lock()  # 写入锁
        self.with_thread_lock = ThreadLock(self.cache_lock, time_out=1 / 60)  # 直接用于 with 的主锁
        self.threaded_write = threading.Timer(1, self._log_file_time_write)  # 基于 timer 的多线程
        # 日志缓存表
        self.log_cache = ListCache(self.with_thread_lock)

    def end_thread(self) -> None:
        """结束日志写入进程，顺手把目前的缓存写入"""
        self.cache_lock.acquire(blocking=True)
        self.write_lock.acquire(blocking=True)
        self.threaded_write.cancel()
        self.started = False
        self._log_file_time_write()
        atexit.unregister(self.end_thread)

    def start_thread(self) -> None:
        self.threaded_write.start()
        self.started = True
        atexit.register(self.end_thread)

    @property
    def logfile_name(self) -> PathLike:
        return self._logfile_name

    @logfile_name.setter
    def logfile_name(self, value: PathLike) -> None:
        with self.with_thread_lock:
            self._logfile_name = value

    def _log_file_time_write(self) -> None:
        """使用 threading.Timer 调用的定时写入日志文件的函数"""
        if self.log_cache:
            with self.with_thread_lock:
                if self.log_cache:
                    with open(file=self.logfile_name, encoding='utf-8', mode='a') as log_file:
                        log_file.writelines(self.log_cache)

    def write_logs(self, string: str, wait_for_cache: bool = True) -> None:
        if not wait_for_cache:
            with self.with_thread_lock and open(file=self.logfile_name, encoding='utf-8', mode='a') as log_file:
                if self.log_cache:
                    log_file.writelines(self.log_cache)
                log_file.write(string)
        else:
            self.log_cache.append(string)


class Logger:
    """shenjack logger"""

    def __init__(self, name: str = None, level: int = None, file_name: PathLike = None, **kwargs) -> None:
        """
        配置模式: 使用 kwargs 配置
        @param name: logger 名称 默认为 root
        @param level: logging 输出等级 默认为 DEBUG(10)
        @param file_name: logging 写入文件名称 默认为 None(不写入)
        """
        self.name = name or 'root'
        self.level = level or DEBUG
        self.colors = None
        if file_name:
            self.file_cache = LogFileCache(file_name=file_name)
        else:
            self.file_cache = False
        self.warn = self.warning

    def make_log(self, *values: object,
                 level: int,
                 sep: Optional[str] = ' ',
                 end: Optional[str] = '\n',
                 flush: Optional[bool] = False) -> None:
        if level < self.level:
            return None
        # print(level, values, sep, end, flush, sep='|')
        write_text = sep.join(i if type(i) is str else str(i) for i in values).__add__(end)
        print(write_text, end='')
        # self.file_cache.write_logs()
        if self.file_cache:
            self.file_cache: LogFileCache
            if not self.file_cache.started:
                self.file_cache.start_thread()

    def trace(self, *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False) -> None:
        return self.make_log(*values, level=TRACE, sep=sep, end=end, flush=flush)

    def fine(self, *values: object,
             sep: Optional[str] = ' ',
             end: Optional[str] = '\n',
             flush: Optional[bool] = False) -> None:
        return self.make_log(*values, level=FINE, sep=sep, end=end, flush=flush)

    def debug(self,
              *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False) -> None:
        return self.make_log(*values, level=DEBUG, sep=sep, end=end, flush=flush)

    def info(self,
             *values: object,
             sep: Optional[str] = ' ',
             end: Optional[str] = '\n',
             flush: Optional[bool] = False) -> None:
        return self.make_log(*values, level=INFO, sep=sep, end=end, flush=flush)

    def warning(self,
                *values: object,
                sep: Optional[str] = ' ',
                end: Optional[str] = '\n',
                flush: Optional[bool] = False) -> None:
        return self.make_log(*values, level=WARNING, sep=sep, end=end, flush=flush)

    def error(self,
              *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False) -> None:
        return self.make_log(*values, level=ERROR, sep=sep, end=end, flush=flush)

    def fatal(self,
              *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False) -> None:
        return self.make_log(*values, level=FATAL, sep=sep, end=end, flush=flush)


def color_in_033(*args) -> str:
    color_text = ';'.join(args)
    color_text = f'\033[{color_text}m'
    return color_text


def rgb(r: int, g: int, b: int) -> Tuple[int, int, int]:
    return r, g, b


def logging_color() -> Dict:
    ...
    return {'info': ..., 'message': ...}


logger_configs = {
    'Logger': {
        'root': {
            'level': TRACE,
            'color': 'main_color',
            'file': 'main_log_file',
        },
    },
    'Color': {
        'main_color': {
            TRACE: {'info': '\033[34;40m', 'message': '\033[48;2;40;40;40m'},
            FINE: {'info': '', 'message': '\033[35m'},
            DEBUG: {'info': '', 'message': '\033[38;2;133;138;149m'},
            INFO: {'info': '\033[32;40m', 'message': ''},
            WARNING: {'info': '', 'mes sage': '\033[33m'},
            ERROR: {'info': '', 'message': '\033[31m'},
            FATAL: {'info': '', 'message': '\033[33;41'}
        }
    },
    'File': {
        'main_log_file': {
            'mode': 'a',
            'encoding': 'utf-8',
            'level': DEBUG,
            'file_name': '{file_time}_logs.md'
        },
    },
    'Formatter': {
        'file_time': {'strftime': '%Y-%m-%d %H-%M'},
        'main_time': {'strftime': '%Y-%m-%d %H-%M-%S'},
        'version': 'game.version',
        'level': 'level',
        'encoding': 'utf-8',
        ...: ...
    }
}


def add_dict_config_to_global(some_dict: Union[dict, list, str], name: str) -> dict:
    """
    提前声明，这个函数很有可能搞坏 config
    请使用 add_kwargs_to_global 来修改配置
    如果你不知道你在改什么，请**务必不要**用这个函数来修改配置
    @param some_dict: 一个你丢进来的 logger 设置
    @param name: 这个 logger 设置的名称
    @return: 修改过的 logger 配置
    """
    logger_configs[name] = some_dict
    return logger_configs  # 修改过的 logger 配置


def add_kwargs_to_global(**kwargs) -> dict:
    """

    @param kwargs: 你要改的 logger配置
    @return: 修改过的 logger 配置
    """
    ...


def get_logger(name: str = 'name') -> Logger:
    """
    此函数用于从 global_config 中取出对应的配置建立一个相应的 logger
    @param name: logger的名称
    @return: 创建好的 logger
    """
    ...


if __name__ == "__main__":
    import os

    os.chdir('../../')
    # 在这里可以使用 add_kwargs_to_global
    logger = Logger(name="Main")
    logger1 = Logger(name="RenderThread")
    logger2 = Logger(name="TaskExecuter#1-1")
    while True:
        logger.info("Hello World!!")
        logger1.error("OpenGL Error 10086")
        logger2.warning("Cannot write file.")
    exit(0)

    some_logger = Logger(name='aaa')
    some_logger.level = ALL
    some_logger.warn('aaaa', 'aaaa')

    a_lock = threading.Lock()
    a_with_lock = ThreadLock(a_lock)
    a_cache = ListCache(a_with_lock)
    a_cache.append('123123')
    print(a_cache[0])
    print(a_cache)
