#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from typing import Optional, Tuple
from pyglet.graphics import Batch, Group

from Difficult_Rocket.client import ClientWindow
from Difficult_Rocket.api.screen import BaseScreen
# from Difficult_Rocket.main import Game
from Difficult_Rocket.gui.widget.button import (
    PressTextButton,
    MinecraftWikiButtonTheme,
)

from lib_not_dr import loggers

# from . import DR_mod_runtime

logger = loggers.config.get_logger_from_old("client.dr_game_layout", "client")

class GameLayout(BaseScreen):
    """
    DR game 的 菜单
    """

    name = "Dr_game_layout"

    def __init__(self, main_window: ClientWindow):
        super().__init__(main_window)
        self.main_batch = Batch()
        self.main_group = Group(parent=main_window.main_group, order=1)

    def on_draw(self, dt: float, window: ClientWindow):
        self.main_batch.draw()
