#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import io
import sys
import time
import string
import atexit
import threading

from pathlib import Path
from typing import Optional

from lib_not_dr.logger import LogLevel
from lib_not_dr.types.options import Options
from lib_not_dr.logger.structure import LogMessage
from lib_not_dr.logger.formatter import BaseFormatter, StdFormatter

__all__ = [
    'BaseOutputStream',
    'StdioOutputStream',
    'FileCacheOutputStream'
]


class BaseOutputStream(Options):
    name = 'BaseOutputStream'

    level: int = LogLevel.info
    enable: bool = True

    formatter: BaseFormatter

    def write_stdout(self, message: LogMessage) -> None:
        raise NotImplementedError(f'{self.__class__.__name__}.write_stdout is not implemented')

    def write_stderr(self, message: LogMessage) -> None:
        raise NotImplementedError(f'{self.__class__.__name__}.write_stderr is not implemented')

    def flush(self) -> None:
        raise NotImplementedError(f'{self.__class__.__name__}.flush is not implemented')

    def close(self) -> None:
        self.enable = False


class StdioOutputStream(BaseOutputStream):
    name = 'StdioOutputStream'

    level: int = LogLevel.info
    formatter: BaseFormatter = StdFormatter()
    use_stderr: bool = True

    def write_stdout(self, message: LogMessage) -> None:
        if not self.enable:
            return None
        if message.level < self.level:
            return None
        print(self.formatter.format_message(message), end='', flush=message.flush)
        return None

    def write_stderr(self, message: LogMessage) -> None:
        if not self.enable:
            return None
        if message.level < self.level:
            return None
        if self.use_stderr:
            print(self.formatter.format_message(message), end='', flush=message.flush, file=sys.stderr)
        else:
            print(self.formatter.format_message(message), end='', flush=message.flush)
        return None

    def flush(self) -> None:
        """
        flush stdout and stderr
        :return: None
        """
        print('', end='', flush=True)
        print('', end='', flush=True, file=sys.stderr)
        return None


class FileCacheOutputStream(BaseOutputStream):
    name = 'FileCacheOutputStream'

    level: int = LogLevel.info
    formatter: BaseFormatter = StdFormatter(enable_color=False)
    text_cache: io.StringIO = None

    flush_counter: int = 0
    # 默认 10 次 flush 一次
    flush_count_limit: int = 10
    flush_time_limit: int = 10  # time limit in sec, 0 means no limit
    flush_timer: threading.Timer = None

    file_path: Optional[Path] = Path('./logs')
    file_name: str
    # file mode: always 'a'
    file_encoding: str = 'utf-8'
    # do file swap or not
    file_swap: bool = False
    at_exit_register: bool = False

    file_swap_counter: int = 0
    file_swap_name_template: str = '${name}-${counter}.log'
    # ${name} -> file_name
    # ${counter} -> file_swap_counter
    # ${log_time} -> time when file swap ( round(time.time()) )
    # ${start_time} -> start time of output stream ( round(time.time()) )
    current_file_name: str = None
    file_start_time: int = None

    # log file swap triggers
    # 0 -> no limit
    file_size_limit: int = 0  # size limit in kb
    file_time_limit: int = 0  # time limit in sec 0
    file_swap_on_both: bool = False  # swap file when both size and time limit reached

    def init(self, **kwargs) -> bool:
        self.file_start_time = round(time.time())
        if self.text_cache is None:
            self.text_cache = io.StringIO()
        self.get_file_path()
        return False

    def _write(self, message: LogMessage) -> None:
        """
        write message to text cache
        默认已经检查过了
        :param message: message to write
        :return: None
        """
        self.text_cache.write(self.formatter.format_message(message))
        self.flush_counter += 1
        if message.flush or self.flush_counter >= self.flush_count_limit:
            self.flush()
        else:
            if self.flush_time_limit > 0:
                if self.flush_timer is None or not self.flush_timer.is_alive():
                    self.flush_timer = threading.Timer(self.flush_time_limit, self.flush)
                    self.flush_timer.daemon = True
                    self.flush_timer.start()
            if not self.at_exit_register:
                atexit.register(self.flush)
                self.at_exit_register = True
        return None

    def write_stdout(self, message: LogMessage) -> None:
        if not self.enable:
            return None
        if message.level < self.level:
            return None
        self._write(message)
        return None

    def write_stderr(self, message: LogMessage) -> None:
        if not self.enable:
            return None
        if message.level < self.level:
            return None
        self._write(message)
        return None

    def get_file_path(self) -> Path:
        """
        get file path
        :return:
        """
        if (current_file := self.current_file_name) is None:
            if not self.file_swap:
                # 直接根据 file name 生成文件
                current_file = Path(self.file_path) / self.file_name
                self.current_file_name = str(current_file)
                return current_file
            template = string.Template(self.file_swap_name_template)
            file_name = template.safe_substitute(name=self.file_name,
                                                 counter=self.file_swap_counter,
                                                 log_time=round(time.time()),
                                                 start_time=self.file_start_time)
            current_file = Path(self.file_path) / file_name
            self.current_file_name = str(current_file)
        else:
            current_file = Path(current_file)
        return current_file

    def check_flush(self) -> Path:
        current_file = self.get_file_path()
        # 获取当前文件的路径
        if not self.file_swap:
            # 不需要 swap 直接返回
            return current_file
        # 检查是否需要 swap
        size_pass = True
        if self.file_size_limit > 0:
            file_size = current_file.stat().st_size / 1024  # kb
            if file_size > self.file_size_limit:  # kb
                size_pass = False
        time_pass = True
        if self.file_time_limit > 0:
            file_time = round(time.time()) - current_file.stat().st_mtime
            if file_time > self.file_time_limit:
                time_pass = False
        if (self.file_swap_on_both and size_pass and time_pass) or \
           (not self.file_swap_on_both and (size_pass or time_pass)):
            # 两个都满足
            # 或者只有一个满足
            if size_pass and time_pass:
                self.file_swap_counter += 1
                # 生成新的文件名
                return self.get_file_path()

    def flush(self) -> None:
        new_cache = io.StringIO()  # 创建新的缓存
        self.flush_counter = 0  # atomic, no lock
        old_cache, self.text_cache = self.text_cache, new_cache
        text = old_cache.getvalue()
        old_cache.close()  # 关闭旧的缓存
        if text == '':
            return None
        current_file = self.check_flush()
        if not current_file.exists():
            current_file.parent.mkdir(parents=True, exist_ok=True)
            current_file.touch(exist_ok=True)
        with current_file.open('a', encoding=self.file_encoding) as f:
            f.write(text)
        return None

    def close(self) -> None:
        super().close()
        self.flush()
        self.text_cache.close()
        atexit.unregister(self.flush)
        return None
