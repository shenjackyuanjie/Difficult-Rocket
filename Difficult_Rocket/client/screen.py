#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import typing

from pyglet.text import Label
from pyglet.graphics import Batch, Group
from pyglet.clock import get_frequency

# Difficult Rocket function
from Difficult_Rocket.api.types import Fonts
# from Difficult_Rocket.utils import translate
from Difficult_Rocket.api.screen import BaseScreen
# from Difficult_Rocket.command.tree import CommandTree

if typing.TYPE_CHECKING:
    from Difficult_Rocket.client import ClientWindow


class DRScreen(BaseScreen):
    def __init__(self, main_window: "ClientWindow"):
        super().__init__(main_window)


class DRDEBUGScreen(BaseScreen):
    def __init__(self, main_window: "ClientWindow"):
        super().__init__(main_window)
        self.main_batch = Batch()
        self.main_group = Group(order=1)
        self.fps_label = Label(x=10, y=main_window.height - 10,
                               width=main_window.width - 20, height=20,
                               anchor_x='left', anchor_y='top',
                               font_name=Fonts.微软等宽无线, font_size=20,
                               multiline=True,
                               batch=self.main_batch, group=self.main_group)
        self.fps_label.text = "11111114514"

    def draw_update(self, tick: float, window: "ClientWindow"):
        self.update_label(window)

    def update_label(self, window: "ClientWindow"):
        now_FPS = get_frequency()
        self.fps_label.text = (
            f'FPS: {window.fps_log.fps: >5.1f}('
            f'{window.fps_log.middle_fps: >5.1f})[{now_FPS: >.7f}]\n '
            f'{window.fps_log.max_fps: >7.1f} '
            f'{window.fps_log.min_fps:>5.1f}'
        )

    def on_resize(self, width, height, window: "ClientWindow"):
        self.fps_label.y = height - 10

    def on_draw(self, *dt, window: "ClientWindow"):
        self.main_batch.draw()
        # print(self.window_pointer.try_if_runs)
