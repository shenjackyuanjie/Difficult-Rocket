"""
:author shenjackyuanjie
:contact 3695888:qq.com
"""
#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import re
import os
import time
import enum
import atexit
import inspect
import threading

from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, FATAL
from types import FrameType
from typing import Optional, Union, Dict, Iterable, Tuple, Any, List

os.system('')
# print(os.path.abspath(os.curdir))

# 如果想要直接使用 logger 来 logging
# 直接调用 logger.debug() 即可
# 默认配置会有
# ----------
# 配置方式一
# 直接使用 logger.Logger()
# 将会创建一个空 logger
# 可以自行通过
# 配置方式二


color_reset_suffix = "\033[0m"
""" 只是用来重置颜色的后缀 """

re_find_color_code = r'\033\[[^\f\n\r\t\vm]*m'
re_color_code = re.compile(re_find_color_code)

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


class LoggingLevel(enum.IntEnum):
    """ 存储 logger 级别的 enum 类"""
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    FINE = 7
    TRACE = 5
    NOTSET = 0
    ALL = NOTSET


level_name_map = {
    ALL:     'ALL',  # NOTSET
    TRACE:   'TRACE',
    FINE:    'FINE',
    DEBUG:   'DEBUG',
    INFO:    'INFO',
    WARNING: 'WARNING',  # WARN
    ERROR:   'ERROR',
    FATAL:   'FATAL'
}

name_level_map = {
    'NOTSET':   ALL,
    'ALL':      ALL,
    'TRACE':    TRACE,
    'FINE':     FINE,
    'DEBUG':    DEBUG,
    'INFO':     INFO,
    'WARNING':  WARNING,
    'WARN':     WARNING,
    'ERROR':    ERROR,
    'CRITICAL': FATAL,
    'FATAL':    FATAL
}

logger_configs = {
    'Logger':    {
        'root':   {
            'level': TRACE,
            'color': 'main_color',
            'file':  'main_log_file',
        },
        'client': {
            'level': TRACE,
            'color': 'main_color',
            # 'file':  'main_log_file',
        },
        'server': {
            'level': TRACE,
            'color': 'DiGua_color',
            'file':  'main_log_file',
        },
    },
    'Color':     {
        'main_color':  {
            'file_time': '\033[38;2;201;222;56m',
            'main_time': '\033[38;2;201;222;56m',
            'file_name': '\033[38;2;0;255;180m',
            'code_line': '\033[38;2;0;255;180m',
            'logger':    '\033[0m',
            TRACE:       {'info': '\033[38;2;138;173;244m', 'message': '\033[38;2;138;173;244m'},
            FINE:        {'info': '\033[35;48;2;44;44;54m', 'message': '\033[35m'},
            DEBUG:       {'info': '\033[38;2;133;138;149m', 'message': '\033[38;2;133;138;149m'},
            INFO:        {'info': '\033[0m', 'message': '\033[0m'},
            WARNING:     {'info': '\033[33m', 'message': '\033[33m'},
            ERROR:       {'info': '\033[31m', 'message': '\033[31m'},
            FATAL:       {'info': '\033[38;2;255;255;0;48;2;120;10;10m', 'message': '\033[38;2;255;255;0;48;2;120;10;10m'}
        },
        'DiGua_color': {
            # catppuccin Macchiato
            'file_time': '\033[38;2;238;212;159m',
            'main_time': '\033[38;2;202;211;245m',
            'file_name': '\033[38;2;139;213;202m',
            'code_line': '\033[38;2;166;218;149m',
            'logger':    '\033[0m',
            TRACE:       {'info': '\033[38;2;138;173;244m', 'message': '\033[38;2;138;173;244m'},
            FINE:        {'info': '\033[38;2;198;160;246m', 'message': '\033[38;2;198;160;246m'},
            DEBUG:       {'info': '\033[38;2;133;138;149m', 'message': '\033[38;2;133;138;149m'},
            INFO:        {'info': '\033[0m', 'message': '\033[0m'},
            WARNING:     {'info': '\033[38;2;245;169;127m', 'message': '\033[38;2;245;169;127m'},
            ERROR:       {'info': '\033[38;2;237;135;150m', 'message': '\033[38;2;237;135;150m'},
            FATAL:       {'info': '\033[38;2;255;255;0;48;2;120;10;10m', 'message': '\033[38;2;255;255;0;48;2;120;10;10m', 'logger': '\033[38;2;245;189;230m'}
        }
    },
    'File':      {
        'main_log_file': {
            'mode':       'a',
            'encoding':   'utf-8',
            'level':      TRACE,
            'file_name':  './logs/{file_time}_logs.md',
            'cache_len':  10,
            'cache_time': 1
        },
    },
    'Formatter': {
        'MESSAGE':   {
            'format': '[{main_time}] [{logger_name}] {level} | {file_name}:{code_line} | {message}'
        },
        'file_name': 'no frame',
        'code_line': 'no frame',
        'file_time': {'strftime': '%Y-%m-%d %H-%M'},
        'main_time': {'strftime': '%Y-%m-%d %H-%M-%S:%%S'},  # %%S  三位毫秒
        ...:         ...
    }
}


class ThreadLock:
    """一个用来 with 的线程锁"""

    def __init__(self, the_lock: threading.Lock, time_out: Union[float, int] = 1 / 60) -> None: ...

    def __enter__(self): ...

    def __exit__(self, exc_type, exc_val, exc_tb): ...


class ListCache:
    """一个线程安全的列表缓存"""

    def __init__(self, lock: ThreadLock): ...

    def append(self, value: Union[str, Iterable[str]]): ...

    def __getitem__(self, item) -> str: ...

    def __call__(self, *args, **kwargs) -> List[str]: ...

    def __iter__(self): ...

    def __next__(self): ...

    def __bool__(self): ...

    :property
    def cache(self): ...

    def clear(self): ...


class LogFileCache:
    """日志文件缓存"""

    def __init__(self, file_conf: dict):
        """

        :param file_conf: 日志文件配置
        """

    def file_setup(self) -> None: ...

    def end_thread(self) -> None:
        """结束日志写入进程，顺手把目前的缓存写入"""

    def start_thread(self) -> None: ...

    :property
    def logfile_name(self) -> str: ...

    :logfile_name.setter
    def logfile_name(self, value: str) -> None: ...

    def _log_file_time_write(self, thread: bool = False) -> None: ...

    def write_logs(self, string: str, flush: bool = False) -> None: ...


class Logger:
    """shenjack logger"""

    def __init__(self,
                 name: str = 'root',
                 level: int = DEBUG,
                 file_conf: List[LogFileCache] = None,
                 colors: Dict[Union[int, str], Dict[str, str]] = None,
                 formats=None) -> None:
        """
        配置模式: 使用 kwargs 配置
        :param name: logger 名称 默认为 root
        :param level: logging 输出等级 默认为 DEBUG(10)
        :param file_conf: logger 的文件处理配置
        :param colors: dict 颜色配置
        :param formats: 格式化配置
        """

    def add_file(self, handler: LogFileCache) -> Nones: ...

    def remove_file(self, handler: LogFileCache) -> None: ...

    def make_log(self, *values: object,
                 level: int,
                 sep: Optional[str] = ' ',
                 end: Optional[str] = '\n',
                 flush: Optional[bool] = False,
                 frame: Optional[FrameType] = None) -> None: ...

    def format_text(self, level: int, text: str, frame: Optional[FrameType]) -> str: ...

    def trace(self, *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False,
              frame: Optional[FrameType] = None) -> None: ...

    def fine(self, *values: object,
             sep: Optional[str] = ' ',
             end: Optional[str] = '\n',
             flush: Optional[bool] = False,
             frame: Optional[FrameType] = None) -> None: ...

    def debug(self,
              *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False,
              frame: Optional[FrameType] = None) -> None: ...

    def info(self,
             *values: object,
             sep: Optional[str] = ' ',
             end: Optional[str] = '\n',
             flush: Optional[bool] = False,
             frame: Optional[FrameType] = None) -> None: ...

    def warning(self,
                *values: object,
                sep: Optional[str] = ' ',
                end: Optional[str] = '\n',
                flush: Optional[bool] = False,
                frame: Optional[FrameType] = None) -> None: ...

    def error(self,
              *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False,
              frame: Optional[FrameType] = None) -> None: ...

    def fatal(self,
              *values: object,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False,
              frame: Optional[FrameType] = None) -> None: ...


def get_key_from_dict(a_dict: Dict, key: Any, default: Any = None) -> Optional[Any]: ...


def format_str(text: str) -> str: ...


def len_without_color_maker(text: str) -> int: ...


def gen_file_conf(file_name: str,
                  file_level: int = DEBUG,
                  file_mode: str = 'a',
                  file_encoding: str = 'utf-8',
                  file_cache_len: int = 10,
                  file_cache_time: Union[int, float] = 1) -> dict:
    """
    生成一个文件配置
    :param file_name: 日志文件名
    :param file_level: 日志文件记录级别
    :param file_mode: 文件模式
    :param file_encoding: 文件编码
    :param file_cache_len: 文件缓存长度
    :param file_cache_time: 文件缓存时间
    :return: 生成的配置
    """
    return {'file_name':  file_name,
            'level':      file_level,
            'mode':       file_mode,
            'encoding':   file_encoding,
            'cache_len':  file_cache_len,
            'cache_time': file_cache_time}


def gen_color_conf(color_name: str = None, **colors) -> dict: ...


def logger_with_default_settings(name: str,
                                 level: int = DEBUG,
                                 file_conf: dict = None,
                                 colors: dict = None,
                                 formats: dict = None) -> Logger:
    return Logger(name=name,
                  level=level,
                  file_conf=[LogFileCache(gen_file_conf(**file_conf))],
                  colors=gen_color_conf(**colors),
                  formats=logger_configs['Formatter'].copy().update(formats))


def add_file_config(conf_name: str,
                    file_name: str,
                    file_level: int = DEBUG,
                    file_mode: str = 'a',
                    file_encoding: str = 'utf-8',
                    file_cache_len: int = 10,
                    file_cache_time: Union[int, float] = 1) -> None:
    """
    向 logger config 里添加一个文件配置
    :param conf_name: 文件配置名称
    :param file_name: 日志文件名
    :param file_level: 日志文件记录级别
    :param file_mode: 文件模式
    :param file_encoding: 文件编码
    :param file_cache_len: 文件缓存长度
    :param file_cache_time: 文件缓存时间
    :return: None
    """
    logger_configs['File'][conf_name] = {'file_name':  file_name,
                                         'level':      file_level,
                                         'mode':       file_mode,
                                         'encoding':   file_encoding,
                                         'cache_len':  file_cache_len,
                                         'cache_time': file_cache_time}


def get_logger(name: str = 'root') -> Logger:
    """
    此函数用于从 global_config 中取出对应的配置建立一个相应的 logger
    :param name: logger的名称 默认为 root
    :return: 创建好的 logger
    """


def test_logger(the_logger: Logger) -> None: ...

