#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from typing import Callable

func_list = []


def mix_tick(func: Callable) -> Callable:
    func_list.append(func)

    def wrapped(game) -> None:
        func()
        return None

    return wrapped

