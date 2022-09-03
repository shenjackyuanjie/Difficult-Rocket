"""
@author shenjackyuanjie
@contact 3695888@qq.com
"""
import re
import os
import sys
import time
import atexit
import inspect
import threading

# from inspect import F
from os import PathLike
from time import strftime
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, FATAL
from types import FrameType
from typing import Optional, Union, Dict, Iterable, Tuple, Any, List, Callable

print(os.path.abspath(os.curdir))
os.chdir('../../')
sys.path.append('D:/githubs/DR')
sys.path.append(os.path.abspath('./Difficult_Rocket'))

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


color_reset_suffix = "\033[0m"
""" 只是用来重置颜色的后缀 """

re_find_color_code = r'\033\[[^\f\n\r\t\vm]*m'

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

logger_configs = {
    'Logger': {
        'root': {
            'level': TRACE,
            'color': 'main_color',
            'file': 'main_log_file',
        },
        'client': {
            'level': TRACE,
            'color': 'main_color',
            'file': 'main_log_file',
        },
        'server': {
            'level': TRACE,
            'color': 'main_color',
            'file': 'main_log_file',
        },
    },
    'Color': {
        'main_color': {
            'date': '\033[38;2;201;222;56m',
            'file': '\033[38;2;0;255;180m',
            'line': '\033[38;2;0;255;180m',
            'logger': '\033[0m',
            TRACE: {'info': '\033[34;48;2;44;44;54m', 'message': '\033[34;48;2;40;40;70m'},
            FINE: {'info': '\033[35;48;2;44;44;54m', 'message': '\033[35m'},
            DEBUG: {'info': '\033[38;2;133;138;149m', 'message': '\033[38;2;133;138;149m'},
            INFO: {'info': '\033[0m', 'message': '\033[0m'},
            WARNING: {'info': '\033[33m', 'message': '\033[33m'},
            ERROR: {'info': '\033[31m', 'message': '\033[31m'},
            FATAL: {'info': '\033[38;2;255;255;0;48;2;120;10;10m', 'message': '\033[38;2;255;255;0;48;2;120;10;10m'}
        }
    },
    'File': {
        'main_log_file': {
            'mode': 'a',
            'encoding': 'utf-8',
            'level': TRACE,
            'file_name': './logs/{file_time}_logs.md'
        },
    },
    'Formatter': {
        'MESSAGE': {
            'format': '[{main_time}] [{logger_name}] {level} | {file_name}:{code_line} | {message}'
        },
        'file_time': {'strftime': '%Y-%m-%d %H-%M'},
        'main_time': {'strftime': '%Y-%m-%d %H-%M-%S:%%S'},  # %%S  三位毫秒
        ...: ...
    }
}


class ListCache:
    """一个线程安全的列表缓存"""

    def __init__(self, lock: ThreadLock):
        self._cache = []
        self.with_thread_lock = lock

    def append(self, value: Union[str, Iterable]):
        with self.with_thread_lock:
            if isinstance(value, str):
                self._cache.append(value)
            elif isinstance(value, Iterable):
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
                raise IndexError(f'there is no cache at {item}!\ncache:{self.cache}\n{exp}')

    def __call__(self, *args, **kwargs):
        return self.cache

    def __iter__(self):
        # with self.with_thread_lock:
        #     self._iter_cache = self._cache.copy()
        #     self._iter_len = len(self.cache)
        self._iter_len = len(self.cache)
        return self

    def __next__(self):
        if self._iter_len == -1:
            del self._iter_len
            raise StopIteration('there is no more cache')
        returns = self.cache[-self._iter_len]
        self._iter_len -= 1
        return returns

    def __bool__(self):
        with self.with_thread_lock:
            return True if len(self.cache) > 0 else False

    @property
    def cache(self):
        return self._cache

    def clear(self):
        with self.with_thread_lock:
            self.cache.clear()


class LogFileCache:
    """日志文件缓存"""

    def __init__(self, file_conf: Dict, flush_time: Optional[Union[int, float]] = 1, log_cache_lens_max: int = 10):
        """

        @param file_conf: 日志文件配置
        @param flush_time: 刷新日志缓存，写入文件的时长间隔
        @param log_cache_lens_max: 日志缓存在自动写入前的最大缓存长度
        """
        # 配置相关
        self._logfile_name = os.path.abspath(format_str(file_conf['file_name']))  # log 文件名称
        self.level = get_key_from_dict(file_conf, 'level', DEBUG)
        self.file_conf = file_conf
        self.flush_time = flush_time  # 缓存刷新时长
        self.cache_entries_num = log_cache_lens_max
        self.started = False
        # 同步锁
        self.cache_lock = threading.Lock()  # 主锁
        self.time_limit_lock = ThreadLock(self.cache_lock, time_out=1 / 60)  # 直接用于 with 的主锁
        self.threaded_write = threading.Timer(1, self._log_file_time_write)  # 基于 timer 的多线程
        # 日志缓存表
        self.log_cache = ListCache(self.time_limit_lock)
        self.file_setup()

    def file_setup(self):
        cache_time = 0
        file_type = self.logfile_name[self.logfile_name.rfind('.'):]
        file_pure_name = self.logfile_name[:self.logfile_name.rfind('.')]
        while os.path.isfile(self.logfile_name):
            cache_time += 1
            self.logfile_name = f'{file_pure_name}-{cache_time}{file_type}'

    def end_thread(self) -> None:
        """结束日志写入进程，顺手把目前的缓存写入"""
        self.cache_lock.acquire(blocking=True)
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
        self._logfile_name: PathLike
        return self._logfile_name

    @logfile_name.setter
    def logfile_name(self, value: PathLike) -> None:
        with self.time_limit_lock:
            self._logfile_name = value

    def _log_file_time_write(self) -> None:
        """使用 threading.Timer 调用的定时写入日志文件的函数"""
        if self.log_cache:
            with self.time_limit_lock:
                if self.log_cache:
                    with open(file=self.logfile_name,
                              encoding=get_key_from_dict(self.file_conf, 'encoding', 'utf-8'),
                              mode=get_key_from_dict(self.file_conf, 'mode', 'a')) as log_file:
                        log_file.writelines(self.log_cache.cache.copy())
                    self.log_cache.clear()

    def write_logs(self, string: str, flush: bool = False) -> None:
        self.log_cache.append(string)
        if len(self.log_cache.cache) >= 10:
            self._log_file_time_write()
            return None
        if flush:
            self._log_file_time_write()
        print(self.log_cache.cache)


class Logger:
    """shenjack logger"""

    def __init__(self, name: str = None, level: int = None, file_conf: Dict = None, colors: Dict[Union[int, str], Dict[str, str]] = None, formats=None, **kwargs) -> None:
        """
        配置模式: 使用 kwargs 配置
        @param name: logger 名称 默认为 root
        @param level: logging 输出等级 默认为 DEBUG(10)
        @param file_name: logging 写入文件名称 默认为 None(不写入)
        """
        self.name = name or 'root'
        self.level = level if level is not None else DEBUG
        self.colors = colors or logger_configs['Color']['main_color']
        self.formats = formats or logger_configs['Formatter']
        if file_conf:
            self.file_cache = LogFileCache(file_conf=file_conf)
            self.file_cache.start_thread()
        else:
            self.file_cache = False
        self.warn = self.warning

    def make_log(self, *values: object,
                 level: int,
                 sep: Optional[str] = ' ',
                 end: Optional[str] = '\n',
                 flush: Optional[bool] = False,
                 frame: Optional[FrameType] = None) -> None:
        # print(level, self.level,
        #       self.file_cache.level if self.file_cache else False,
        #       level >= self.level,
        #       self.file_cache and (level >= self.file_cache.level))
        if level < self.level and self.file_cache and (level < self.file_cache.level):
            return None
        if not frame:
            frame = inspect.currentframe()
            frame = frame.f_back.f_back
        elif (frame := inspect.currentframe()) is not None:
            frame = frame.f_back
        text = sep.join(i if type(i) is str else str(i) for i in values)
        text = f"{self.colors[level]['message']}{text}{color_reset_suffix}"
        print_text = self.format_text(level=level, text=text, frame=frame)
        if level >= self.level:
            print(print_text, end=end)
        if self.file_cache and (level >= self.file_cache.level):
            self.file_cache: LogFileCache
            self.file_cache.write_logs(f"{re.sub(re_find_color_code, '', print_text)}{end}", flush=flush)
        return None

    def format_text(self, level: int, text: str, frame: Optional[FrameType]) -> str:
        from Difficult_Rocket import DR_option, DR_runtime
        level_with_color = f"[{self.colors[level]['info']}{level_name_map[level]}{color_reset_suffix}]"
        level_with_color = f"{level_with_color}{' ' * (9 - len_without_color_maker(level_with_color))}"
        formats = self.formats.copy()
        formats.pop('MESSAGE')
        if frame is None:
            formats['file_name'] = 'no frame'
            formats['code_line'] = 'no frame'
        else:
            formats['file_name'] = f"{self.colors['file']}{os.path.split(frame.f_code.co_filename)[-1]}{color_reset_suffix}"
            formats['code_line'] = f"{self.colors['line']}{frame.f_lineno}{color_reset_suffix}"
        now_time = str(time.time())
        for key, value in formats.items():
            if isinstance(value, dict):
                if 'strftime' in value:
                    value['strftime']: str
                    formats[key] = f"{self.colors['date']}{strftime(value['strftime'].replace('%%S', now_time[now_time.find('.') + 1:now_time.find('.') + 4]))}{color_reset_suffix}"
        print_text = self.formats['MESSAGE']['format'].format(level_with_color=level_with_color,
                                                              level=level_with_color, message=text,
                                                              logger_name=self.name,
                                                              **formats)
        return print_text

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


def get_key_from_dict(a_dict: Dict, key: Any, default: Any = None) -> Optional[Any]:
    try:
        return a_dict[key]
    except KeyError:
        return default


def format_str(text: str) -> str:
    formats = logger_configs['Formatter'].copy()
    now_time = str(time.time())
    for key, value in formats.items():
        if isinstance(value, dict):
            if 'strftime' in value:
                value['strftime']: str
                formats[key] = strftime(value['strftime'].replace('%%S', now_time[now_time.find('.') + 1:now_time.find('.') + 4]))
    return text.format(**formats)


def color_in_033(*args) -> str:
    color_text = ';'.join(args)
    color_text = f'\033[{color_text}m'
    return color_text


def len_without_color_maker(text: str) -> int:
    with_out_text = re.sub(re_find_color_code, '', text)
    return len(with_out_text)


def rgb(r: int, g: int, b: int) -> Tuple[int, int, int]:
    return r, g, b


def logging_color() -> Dict:
    ...
    return {'info': ..., 'message': ...}


def setup_logger() -> None:
    ...


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


def get_logger(name: str = 'root') -> Logger:
    """
    此函数用于从 global_config 中取出对应的配置建立一个相应的 logger
    @param name: logger的名称
    @return: 创建好的 logger
    """
    if name in logger_configs['Logger']:
        the_config = logger_configs['Logger'][name]
    else:
        the_config = logger_configs['Logger']['root']
    a_logger = Logger(name=name,
                      level=the_config['level'],
                      file_conf=logger_configs['File'][the_config['file']] if 'file' in the_config else None,
                      colors=logger_configs['Color'][get_key_from_dict(the_config, 'color', 'main_color')],
                      formats=logger_configs['Formatter'])
    return a_logger


if __name__ == "__main__":
    os.chdir('githubs/DR')
    # 在这里可以使用 add_kwargs_to_global
    logger = Logger(name="Main", level=NOTSET)
    for x in range(5):
        logger.trace('tracing')
        logger.fine('some fine!')
        logger.debug('debugging')
        logger.info("Hello World!!")
        logger.warn('warning')
        logger.error('error haaaa')
        logger.fatal('oh no')
    a_logger = get_logger('client')
    a_logger.trace('tracing')
    # time.sleep(5)
    a_logger.fine('some fine!')
    a_logger.debug('debugging')
    # time.sleep(5)
    a_logger.info("Hello World!!")
    a_logger.warn('warning')
    a_logger.error('error haaaa')
    a_logger.fatal('oh no')
    for x in range(5):
        a_logger.trace('tracing')
        a_logger.fine('some fine!')
        a_logger.debug('debugging')
        a_logger.info("Hello World!!")
        a_logger.warn('warning')
        a_logger.error('error haaaa')
        a_logger.fatal('oh no')
