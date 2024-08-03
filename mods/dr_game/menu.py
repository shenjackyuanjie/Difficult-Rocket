#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

# from typing import Optional, Tuple
from pyglet.graphics import Batch, Group

from Difficult_Rocket.client import ClientWindow
from Difficult_Rocket.api.screen import BaseScreen

# from Difficult_Rocket.main import Game
from Difficult_Rocket.gui.widget.button import (
    OreuiButton,
    OreuiButtonStyles,
)

from lib_not_dr import loggers

# from pyglet.text import Label

# from . import DR_mod_runtime

logger = loggers.config.get_logger_from_old("client.dr_game_menu", "client")


class Menu(BaseScreen):
    """
    DR game 的 菜单
    """

    name = "DR_game_menu"

    def __init__(self, main_window: ClientWindow):
        super().__init__(main_window)
        self.main_batch = Batch()
        self.main_group = Group(parent=main_window.main_group, order=1)

        # 占位, 高二看看能不能咕出来点啥 (20230911)
        # 欸呀, 正好是 911 纪念日哦
        # 好, 高二 第一学期 期末都考完了, 我过来做测试了 (20240119)
        # 高二, 马上要研学了, 似乎做了点啥, 但似乎又没做点啥 (20240526)
        # 高二最后一个暑假都过了一半了, 可算把按钮好歹写完了 (20240804)

        self.enter_ship_editor_button = OreuiButton(
            x=100,
            y=100,
            width=150,
            height=30,
            text="进入编辑器aaaa",
            toggle_mode=False,
            auto_release=True,
            batch=self.main_batch,
            group=self.main_group,
        )

        def on_release(x, y):
            from .sr1_ship import SR1ShipEditor, SR1ShipSelecter
            main_window.remove_sub_screen("DR_game_menu")
            main_window.add_sub_screen(SR1ShipEditor.name, SR1ShipEditor)
            main_window.add_sub_screen(SR1ShipSelecter.name, SR1ShipSelecter)
            logger.info("added SR1_ship screen", tag="dr_game")

        self.enter_ship_editor_button.set_handler("on_release", on_release)
        main_window.push_handlers(self.enter_ship_editor_button)

    def on_draw(self, window: ClientWindow):
        self.main_batch.draw()
