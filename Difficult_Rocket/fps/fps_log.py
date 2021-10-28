#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import time
import decimal

from decimal import Decimal

from ..api import new_thread

from libs import pyglet

"""
fps_list ->
[
[fps, time_ns, tick time_ns, pyglet tick]
]
"""


class FpsLogger:
    def __init__(self,
                 stable_fps: int = 60,
                 wait_time: int = 5):
        self.stable_fps = stable_fps
        self.wait_time = wait_time
        self.fps_list = [[stable_fps, time.time_ns()]]
        self._max_fps = stable_fps
        self._min_fps = stable_fps
        self.check_list = True
        self.update_list()

    # @new_thread('fps_logger update', daemon=False, log_thread=False)
    def update_tick(self,
                    tick: Decimal):
        now_time = time.time_ns()
        now_fps = pyglet.clock.get_fps()
        self._max_fps = max(self._max_fps, int(now_fps))
        self._min_fps = min(self._min_fps, int(now_fps))
        tick_time = now_time - self.fps_list[-1][1]
        self.fps_list.append([now_fps, now_time, tick_time, tick])
        if now_time - self.fps_list[0][1] >= self.wait_time * (10 ** 9):
            self.fps_list.pop(0)

    @new_thread('fps_logger check_list', daemon=True)
    def update_list(self):
        while self.check_list:
            now_time = time.time_ns()
            for fps_time in self.fps_list:
                if now_time - fps_time[1] >= self.wait_time * (10 ** 9):
                    del self.fps_list[self.fps_list.index(fps_time)]
            time.sleep(1)

    @property
    def max_fps(self):
        return self._max_fps

    @property
    def min_fps(self):
        return self._min_fps

