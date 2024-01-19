#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from pyglet.graphics import Batch, Group

from Difficult_Rocket.client import ClientWindow
from Difficult_Rocket.api.screen import BaseScreen

from Difficult_Rocket.gui.widget.button import PressTextButton, MinecraftWikiButtonTheme

# from . import DR_mod_runtime


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

        self.main_button = PressTextButton(
            x=200,
            y=300,
            width=150,
            height=30,
            text="test button",
            batch=self.main_batch,
            group=self.main_group,
            draw_theme=MinecraftWikiButtonTheme,
        )
        self.button2 = PressTextButton(
            x=200,
            y=200,
            width=150,
            height=30,
            text="test button",
            batch=self.main_batch,
            group=self.main_group,
        )
        main_window.push_handlers(self.main_button)
        main_window.push_handlers(self.button2)

    def on_draw(self, dt: float, window: ClientWindow):
        self.main_batch.draw()

