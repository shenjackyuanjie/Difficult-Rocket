#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import functools
import inspect
import threading
from threading import Lock
from typing import Optional, Callable, Union, List

from Difficult_Rocket.exception.threading import LockTimeOutError

__all__ = [
    'new_thread',
    'FunctionThread',
    'ThreadLock',
    'record_thread',
    'record_destination',
]

record_thread = False
record_destination: List[Callable[['FunctionThread'], None]] = []


class ThreadLock:

    def __init__(self, the_lock: Lock, time_out: Union[float, int] = 1 / 60) -> None:
        self.lock = the_lock
        self.time_out = time_out

    def __enter__(self):
        self.lock.acquire(timeout=self.time_out)
        if not self.lock.locked():
            raise LockTimeOutError(f'Lock time Out with {self.time_out}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.lock.locked():
            self.lock.release()


"""
This part of code come from MCDReforged(https://github.com/Fallen-Breath/MCDReforged)
Very thanks to Fallen_Breath and other coder who helped MCDR worked better
GNU Lesser General Public License v3.0（GNU LGPL v3)
(have some changes)
"""


def copy_signature(target: Callable, origin: Callable) -> Callable:
    """
    Copy the function signature of origin into target
    """
    # https://stackoverflow.com/questions/39926567/python-create-decorator-preserving-function-arguments
    target.__signature__ = inspect.signature(origin)
    return target


class FunctionThread(threading.Thread):
    """
    A Thread subclass which is used in decorator :func:`new_thread` to wrap a synchronized function call
    """
    __NONE = object()

    def __init__(self, target, name, args, kwargs, daemon):
        super().__init__(target=target, args=args, kwargs=kwargs, name=name, daemon=daemon)
        self.__return_value = self.__NONE
        self.__error = None

        def wrapped_target(*args_, **kwargs_):
            try:
                self.__return_value = target(*args_, **kwargs_)
            except Exception as e:
                self.__error = e
                raise e from None

        self._target = wrapped_target

    def get_return_value(self, block: bool = False, timeout: Optional[float] = None):
        """
        Get the return value of the original function

        If an exception has occurred during the original function call, the exception will be risen again here

        Examples::

            >>> import time
            >>> @new_thread
            ... def do_something(text: str):
            ... 	time.sleep(1)
            ... 	return text

            >>> do_something('task').get_return_value(block=True)
            'task'

        :param block: If it should join the thread before getting the return value to make sure the function invocation finishes
        :param timeout: The maximum timeout for the thread join
        :raise RuntimeError: If the thread is still alive when getting return value. Might be caused by ``block=False``
            while the thread is still running, or thread join operation times out
        :return: The return value of the original function
        """
        if block:
            self.join(timeout)
        if self.__return_value is self.__NONE:
            if self.is_alive():
                raise RuntimeError('The thread is still running')
            raise self.__error
        return self.__return_value


def new_thread(arg: Optional[Union[str, Callable]] = None,
               daemon: bool = False,
               log_thread: bool = True):
    """
    This is a one line solution to make your function executes in parallels.
    When decorated with this decorator, functions will be executed in a new daemon thread

    This decorator only changes the return value of the function to the created ``Thread`` object.
    Beside the return value, it reserves all signatures of the decorated function,
    so you can safely use the decorated function as if there's no decorating at all

    It's also a simple compatible upgrade method for old MCDR 0.x plugins

    The return value of the decorated function is changed to the ``Thread`` object that executes this function

    The decorated function has 1 extra field:

    * ``original`` field: The original undecorated function

    Examples::

        >>> import time

        >>> @new_thread('My Plugin Thread')
        ... def do_something(text: str):
        ... 	time.sleep(1)
        ... 	print(threading.current_thread().name)
        >>> callable(do_something.original)
        True
        >>> t = do_something('foo')
        >>> isinstance(t, FunctionThread)
        True
        >>> t.join()
        My Plugin Thread

    :param arg: A :class:`str`, the name of the thread. It's recommend to specify the thread name, so when you
        log something by ``server.logger``, a meaningful thread name will be displayed
        instead of a plain and meaningless ``Thread-3``
    :param daemon: If the thread should be a daemon thread
    :param log_thread: If the thread should be logged to callback defined in record_destination
    """

    def wrapper(func):
        @functools.wraps(func)  # to preserve the origin function information
        def wrap(*args, **kwargs):
            thread = FunctionThread(target=func, args=args, kwargs=kwargs, name=thread_name, daemon=daemon)
            if record_thread:
                for destination in record_destination:
                    destination(thread)
            thread.start()
            return thread

        # bring the signature of the func to the wrap function
        # so inspect.getfullargspec(func) works correctly
        copy_signature(wrap, func)
        wrap.original = func  # access this field to get the original function
        return wrap

    # Directly use @new_thread without ending brackets case, e.g. @new_thread
    if isinstance(arg, Callable):
        thread_name = None
        return wrapper(arg)
    # Use @new_thread with ending brackets case, e.g. @new_thread('A'), @new_thread()
    else:
        thread_name = arg
        return wrapper


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
