import functools
import inspect
import threading
from Difficult_Rocket import crash
from typing import Optional, Callable


"""
This part of code come from MCDReforged(https://github.com/Fallen-Breath/MCDReforged)
Very thanks to Fallen_Breath and other coder who helped MCDR worked better
GNU Lesser General Public License v3.0（GNU LGPL v3)
(have some changes)
"""

__all__ = [
    'new_thread',
    'FunctionThread'
]


def copy_signature(target: Callable, origin: Callable) -> Callable:
    """
    Copy the function signature of origin into target
    """
    # https://stackoverflow.com/questions/39926567/python-create-decorator-preserving-function-arguments
    target.__signature__ = inspect.signature(origin)
    return target


class FunctionThread(threading.Thread):
    __NONE = object()

    def __init__(self, target, name, args, kwargs):
        super().__init__(target=target, args=args, kwargs=kwargs, name=name)
        self.__return_value = self.__NONE
        self.__error = None

        def wrapped_target(*args_, **kwargs_):
            try:
                self.__return_value = target(*args_, **kwargs_)
            except Exception as e:
                self.__error = e
                print(e)
                raise e from None

        self._target = wrapped_target

    def get_return_value(self, block: bool = False, timeout: Optional[float] = None):
        if block:
            self.join(timeout)
        if self.__return_value is self.__NONE:
            if self.is_alive():
                raise RuntimeError('The thread is still running')
            raise self.__error
        return self.__return_value
    
    def join(self, timeout: Optional[float] = None) -> None:
        super().join(timeout)

    def start(self) -> None:
        super().start()



def new_thread(thread_name: Optional[str or Callable] = None,
               daemon: bool = False,
               log_thread: bool = True):
    """
    Use a new thread to execute the decorated function
    The function return value will be set to the thread instance that executes this function
    The name of the thread can be specified in parameter
    """
    def wrapper(func):
        @functools.wraps(func)  # to preserve the origin function information
        def wrap(*args, **kwargs):
            thread = FunctionThread(target=func, args=args, kwargs=kwargs, name=thread_name)
            thread.daemon = daemon
            thread.start()
            if log_thread:
                crash.all_thread.append(thread)
            return thread
        # bring the signature of the func to the wrap function
        # so inspect.getfullargspec(func) works correctly
        copy_signature(wrap, func)
        wrap.original = func  # access this field to get the original function
        return wrap
    # Directly use @on_new_thread without ending brackets case
    if isinstance(thread_name, Callable):
        this_is_a_function = thread_name
        thread_name = None
        return wrapper(this_is_a_function)
    # Use @on_new_thread with ending brackets case
    return wrapper

