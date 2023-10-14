#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import time

from pathlib import Path
from types import FrameType
from typing import List, Optional, Tuple, Dict, Union

from lib_not_dr.types.options import Options

__all__ = ['LogMessage',
           'FormattingMessage']


class LogMessage(Options):
    name = 'LogMessage'

    # 消息内容本身的属性
    messages: List[str] = []
    end: str = '\n'
    split: str = ' '

    # 消息的属性
    flush: bool = None
    level: int = 20
    log_time: float = None  # time.time_ns()
    logger_name: str = 'root'
    logger_tag: Optional[str] = None
    stack_trace: Optional[FrameType] = None

    def __init__(self,
                 messages: Optional[List[str]] = None,
                 end: Optional[str] = '\n',
                 split: Optional[str] = ' ',
                 flush: Optional[bool] = None,
                 level: Optional[int] = 20,
                 log_time: Optional[float] = None,
                 logger_name: Optional[str] = 'root',
                 logger_tag: Optional[str] = None,
                 stack_trace: Optional[FrameType] = None,
                 **kwargs) -> None:
        """
        Init for LogMessage
        :param messages: message list for log
        :param end: end of message
        :param split: split for messages
        :param flush: do flush or not
        :param level: level of message
        :param log_time: time of message (default: time.time_ns())
        :param logger_name: name of logger
        :param logger_tag: tag of logger
        :param stack_trace: stack trace of logger
        :param kwargs: other options
        """
        # 为了方便使用 单独覆盖了 __init__ 方法来提供代码补全的选项
        super().__init__(messages=messages,
                         end=end,
                         split=split,
                         flush=flush,
                         level=level,
                         log_time=log_time,
                         logger_name=logger_name,
                         logger_tag=logger_tag,
                         stack_trace=stack_trace,
                         **kwargs)

    def init(self, **kwargs) -> bool:
        if self.log_time is None:
            self.log_time = time.time_ns()
        if not isinstance(self.flush, bool) and self.flush is not None:
            self.flush = True if self.flush else False
        return False

    def format_message(self) -> str:
        return self.split.join(self.messages) + self.end

    def format_for_message(self) -> Dict[str, str]:
        basic_info = self.option()

        if self.logger_tag is None:
            basic_info['logger_tag'] = '   '

        basic_info['messages'] = self.format_message()

        return basic_info

    @property
    def create_msec_3(self) -> int:
        return int(self.log_time / 1000000) % 1000


FormattingMessage = Tuple[LogMessage, Dict[str, Union[str, Path]]]

if __name__ == '__main__':
    print(LogMessage().as_markdown())
