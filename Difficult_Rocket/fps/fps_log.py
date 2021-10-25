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

    def update_tick(self,
                    tick: Decimal):
        now_time = time.time_ns()
        now_fps = pyglet.clock.get_fps()
        tick_time = now_time - self.fps_list[-1][1]
        self.fps_list.append([now_fps, now_time, tick_time, tick])
        if now_time - self.fps_list[0][1] >= self.wait_time * (10 ** 9):
            self.fps_list.pop(0)

    @property
    def max_fps(self):
        fps_list = [fpss[0] for fpss in self.fps_list]
        return max(fps_list)

    @property
    def min_fps(self):
        fps_list = [fpss[0] for fpss in self.fps_list]
        return min(fps_list)

