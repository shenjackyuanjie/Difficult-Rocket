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

    def __init__(self, the_lock: Lock, time_out: Union[float, int] = 1 / 60) -> None:
        self.lock = the_lock
        self.time_out = time_out

    def __enter__(self):
        # print('enter!')
        self.lock.acquire(timeout=self.time_out)
        if not self.lock.locked():
            raise LockTimeOutError('')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.lock.locked():
            self.lock.release()
        if (exc_type is None) and (exc_val is None) and (exc_tb is None):
            # 没有出 bug
            # print('exit with no error')
            return None
        else:
            # 出 bug 了
            # print(f'exit with error {exc_type} {exc_val}')
            return None

    # def __del__(self):
    # print('del me!')
    # self.__del__()


if __name__ == "__main__":
    from Difficult_Rocket.exception import TestError

    thread_lock = Lock()

    test_lock = ThreadLock(thread_lock)
    with test_lock:
        print('do some thing')
        ...
    with test_lock:
        print('do some error')
        raise TestError('ah lock test')
