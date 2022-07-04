import atexit
import threading
from time import strftime
from typing import Optional

from Difficult_Rocket.exception.logger import LogFileLockTimeOutError

color_reset_suffix = "\033[0m"


class LogFileCache:
    """日志文件缓存"""

    def __init__(self, file_name: str = 'logs//log.log', flush_time: Optional[int, float] = 1, cache_entries_num: int = 10):
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

    @property
    def logfile_name(self) -> str:
        return self._logfile_name

    @logfile_name.setter
    def logfile_name(self, value: str) -> None:
        with self.thread_lock.acquire(timeout=1/60):
            ...
        self.thread_lock.acquire(timeout=1/60)
        if not self.thread_lock.locked():
            ...

    def _log_file_time_write(self) -> None:
        """使用 threading.Timer 调用的定时写入日志文件的函数"""

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

    def __init__(self, config: dict = None) -> None:
        if config is None:
            self.config = {}
        else:
            self.config = config


class LoggerManager:
    """shenjack牌logger"""

    def __init__(self):
        self.configs = {}

    def add_config(self, name: str, config: dict) -> dict:
        self.configs[name] = config
        return self.configs

    def get_logger(self, name: str = 'root', config: dict = None) -> Logger:
        """相当于 logging.getLogger(name='root')"""
        if not config is None:
            self.add_config(name, config)
        return Logger(config=self.configs)

logger_manager = LoggerManager()
get_logger = logger_manager.get_logger
# shenjack.get_logger()