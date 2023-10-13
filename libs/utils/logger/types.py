#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import time

from types import FrameType
from typing import List, Optional

from lib_not_dr.types.options import Options


class LogMessage(Options):
    name = 'LogMessage'

    # 消息内容本身的属性
    messages: List[str] = []
    end: str = '\n'
    split: str = ' '

    # 消息的属性
    flush: bool = True
    level: int = 20
    log_time: float = time.time_ns()
    logger_name: str = 'root'
    logger_tag: Optional[str] = None
    stack_trace: Optional[FrameType] = None


# [App -> Logger +-> Handler(Formatter)] -> Queue(log) -> [(File, Socket) Output] ?
#                |-> Handler(Formatter) -> Console Output
