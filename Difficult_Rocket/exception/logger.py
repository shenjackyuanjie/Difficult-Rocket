#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from Difficult_Rocket.exception.threading import LockTimeOutError

__all__ = ["LogFileLockTimeOutError"]


class LogFileLockTimeOutError(LockTimeOutError):
    """日志文件写入锁超时"""
