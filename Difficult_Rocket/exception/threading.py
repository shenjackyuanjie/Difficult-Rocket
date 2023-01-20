#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
from Difficult_Rocket.exception import BaseRuntimeError

__all__ = ["LockTimeOutError"]


class LockTimeOutError(BaseRuntimeError):
    """没有特殊指定的 ”某个“ 锁超时了"""
