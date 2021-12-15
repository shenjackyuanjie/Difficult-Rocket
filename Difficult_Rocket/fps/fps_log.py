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
import statistics

from typing import Union
from decimal import Decimal

from libs.pyglet import clock


class FpsLogger:
    def __init__(self,
                 stable_fps: int = 60,
                 count: int = 400):
        self.stable_fps = stable_fps
        self.count = count
        self._fps = stable_fps
        self.middle_fps = stable_fps
        self.fps_list = [stable_fps]  # type: list[Union[int, float]]
        self.get_fps_list = [stable_fps]  # type: list[Union[int, float]]
        self._max_fps = stable_fps
        self._min_fps = stable_fps


    def update_tick(self,
                    tick: Decimal):
        now_fps = clock.get_fps()
        if now_fps != 0:
            self.fps_list.append(now_fps)
        else:
            self.fps_list.append(1)
        if len(self.fps_list) > self.count:
            self.fps_list = self.fps_list[-self.count + 1:]
        if len(self.get_fps_list) > self.count:
            self.get_fps_list = self.get_fps_list[-self.count + 1:]
        try:
            self._fps = statistics.geometric_mean(self.fps_list[-200:])
            self.middle_fps = statistics.median(self.fps_list)
        except Exception:
            print(self.fps_list)
            raise
        self._max_fps = max(self.fps_list)
        self._min_fps = min(self.fps_list)
        # 获取新fps
        del now_fps

    @property
    def max_fps(self):
        return self._max_fps

    @property
    def min_fps(self):
        return self._min_fps

    @property
    def fps(self):
        return self._fps
