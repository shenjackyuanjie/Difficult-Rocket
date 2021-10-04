import functools
import inspect
import threading
from typing import Optional, Callable
from Difficult_Rocket import crash

"""
This part of code come from MCDReforged(https://github.com/Fallen-Breath/MCDReforged)
Very thanks to Fallen_Breath and other coder who helped MCDR worked better
GNU Lesser General Public License v3.0（GNU LGPL v3)
(have some changes)
"""


def new_thread(thread_name: Optional[str or Callable] = None, Daemon=False):
    """
    Use a new thread to execute the decorated function
    The function return value will be set to the thread instance that executes this function
    The name of the thread can be specified in parameter
    """

    def wrapper(func):
        @functools.wraps(func)  # to preserve the origin function information
        def wrap(*args, **kwargs):
            thread_ = threading.Thread(target=func, args=args, kwargs=kwargs, name=thread_name)
            thread_.setDaemon(Daemon)
            thread_.start()
            crash.all_thread.append(thread_)
            return thread_

        # bring the signature of the func to the wrap function
        # so inspect.getfullargspec(func) works correctly
        # https://stackoverflow.com/questions/39926567/python-create-decorator-preserving-function-arguments
        wrap.__signature__ = inspect.signature(func)
        return wrap

    # Directly use @on_new_thread without ending brackets case
    if isinstance(thread_name, Callable):
        this_is_a_function = thread_name
        thread_name = None
        return wrapper(this_is_a_function)
    # Use @on_new_thread with ending brackets case
    return wrapper
