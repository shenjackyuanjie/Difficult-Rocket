"""
@author shenjackyuanjie
@contact 3695888@qq.com
"""
import atexit
import threading

from time import strftime
from typing import Optional, Union, Dict, Iterable, Tuple, List
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, FATAL

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
        # 日志缓存表
        self._log_cache = []
        # 同步锁
        self.cache_lock = threading.Lock()  # 主锁
        self.write_lock = threading.Lock()  # 写入锁
        self.with_thread_lock = ThreadLock(self.cache_lock, time_out=1 / 60)  # 直接用于 with 的主锁
        self.threaded_write = threading.Timer(1, self._log_file_time_write)  # 基于 timer 的多线程

    def end_thread(self) -> None:
        """结束日志写入进程，顺手把目前的缓存写入"""
        self.cache_lock.acquire(blocking=True)
        self.threaded_write.cancel()
        self._log_file_time_write()

    def start_thread(self) -> None:
        self.threaded_write.start()
        atexit.register(self.end_thread)

    @property
    def logfile_name(self) -> str:
        return self._logfile_name

    @logfile_name.setter
    def logfile_name(self, value: str) -> None:
        with self.with_thread_lock:
            self._logfile_name = value

    @property
    def log_caches(self) -> list:
        return self._log_cache

    @log_caches.setter
    def log_caches(self, value: Union[str, Iterable[str]]):
        if type(value) == str:
            with self.with_thread_lock:
                self._log_cache.append(value)
                return
        elif isinstance(value, Iterable):
            with self.with_thread_lock:
                list(map(self._log_cache.append, value))
        ...

    def _log_file_time_write(self) -> None:
        """使用 threading.Timer 调用的定时写入日志文件的函数"""
        if self.log_caches:
            with self.with_thread_lock:
                if self.log_caches:
                    ...

        ...

    def write_logs(self, string: str, wait_for_cache: bool = True) -> None:
        if wait_for_cache:
            with self.with_thread_lock and open(file=self.logfile_name, encoding='utf-8', mode='a') as log_file:
                log_file.writelines(self._log_cache)
                log_file.write(string)
            ...
        else:
            ...


class Logger:
    """shenjack logger"""

    def __init__(self, **kwargs) -> None:
        """
        配置模式: 使用 kwargs 配置
        @param config: 字典格式的配置
        @param kwargs: key word 格式的配置
        """
        self.name = 'root'
        self.level = DEBUG
        self.colors = None
        if kwargs is not None:  # 使用 kwargs 尝试配置
            if name := kwargs.pop('name', False):  # 顺手把获取到的配置填入临时变量 如果成功获取再填入 self
                self.name = name
            if level := kwargs.pop('level', False):
                self.level = level
        else:

            ...

        self.file_cache = LogFileCache()
        self.warn = self.warning
        self.fine = self.detail

    def make_log(self, *values: object,
                 level: int,
                 sep: Optional[str] = ' ',
                 end: Optional[str] = '\n',
                 flush: Optional[bool] = False) -> None:
        if level < self.level:
            return None
        print(level, values, sep, end, flush, sep='|')
        write_text = sep.join(values)
        print(write_text)
        ...

    def detail(self, *values: object,
               sep: Optional[str] = ' ',
               end: Optional[str] = '\n',
               flush: Optional[bool] = False) -> None:
        self.make_log(*values, level=DETAIL, sep=sep, end=end, flush=flush)

    def debug(self,
              *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False) -> None:
        self.make_log(*values, level=DEBUG, sep=sep, end=end, flush=flush)

    def info(self,
             *values: object,
             sep: Optional[str] = ' ',
             end: Optional[str] = '\n',
             flush: Optional[bool] = False) -> None:
        self.make_log(*values, level=INFO, sep=sep, end=end, flush=flush)

    def warning(self,
                *values: object,
                sep: Optional[str] = ' ',
                end: Optional[str] = '\n',
                flush: Optional[bool] = False) -> None:
        self.make_log(*values, level=WARNING, sep=sep, end=end, flush=flush)

    def error(self,
              *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False) -> None:
        self.make_log(*values, level=ERROR, sep=sep, end=end, flush=flush)

    def fatal(self,
              *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False) -> None:
        self.make_log(*values, level=FATAL, sep=sep, end=end, flush=flush)


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
            'color': {
                DEBUG: '\033[0m'
            },
            'file': 'main_log_file',
        },
    },
    'Color': {
        TRACE: {'info': '', 'message': '\033[48;2;40;40;40m'},
        DEBUG: {'info': '', 'message': '\033[32;40m'},
        INFO: {'info': '', 'message': '\033[33;40m'},
        WARNING: {'info': '', 'message': ''},
        ERROR: {'info': '', 'message': ''},
        FATAL: {'info': '', 'message': ''}
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
    # 在这里可以使用 add_kwargs_to_global
    some_logger = Logger(name='aaa')
    some_logger.level = DETAIL
    some_logger.warn('aaaa', 'aaaa')
    ...
