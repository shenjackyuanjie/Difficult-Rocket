#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import threading

from typing import Union
from threading import Lock

from Difficult_Rocket import crash
from Difficult_Rocket.exception.threading import LockTimeOutError


class Threads(threading.Thread):
    def run(self):
        if crash.record_thread:
            crash.all_thread.append(self)
        super().run()


class ThreadLock:

    def __init__(self, the_lock: Lock) -> None:
        self.lock = the_lock

    def __enter__(self, timeout: Union[float, int] = 1/60):
        self.lock.acquire(timeout=timeout)
        if not self.lock.locked():
            raise LockTimeOutError

    def __exit__(self, exc_type, exc_val, exc_tb):
        if (exc_type is None) and (exc_val is None) and (exc_tb is None):
            # 没有出 bug
            self.lock.release()
            return None
        else:
            # 出 bug 了
            self.lock.release()
            return None


if __name__ == "__main__":

    thread_lock = Lock()

    test_lock = ThreadLock(thread_lock)

    with test_lock:
        ...

