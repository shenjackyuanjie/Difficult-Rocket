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

        self.wiki_button1 = PressTextButton(
            x=200,
            y=300,
            width=150,
            height=30,
            text="wiki button1",
            batch=self.main_batch,
            group=self.main_group,
            draw_theme=MinecraftWikiButtonTheme,
            dict_theme={"pop_out": True},
        )
        self.wiki_button2 = PressTextButton(
            x=400,
            y=300,
            width=150,
            height=30,
            text="wiki button2",
            batch=self.main_batch,
            group=self.main_group,
            draw_theme=MinecraftWikiButtonTheme,
            dict_theme={"pop_out": False},
        )
        self.wiki_button3 = PressTextButton(
            x=200,
            y=250,
            width=150,
            height=30,
            text="wiki button3",
            batch=self.main_batch,
            group=self.main_group,
            draw_theme=MinecraftWikiButtonTheme,
            dict_theme={"pop_out": True, "drag_list": True},
        )
        self.wiki_button4 = PressTextButton(
            x=400,
            y=250,
            width=150,
            height=30,
            text="wiki button4",
            batch=self.main_batch,
            group=self.main_group,
            draw_theme=MinecraftWikiButtonTheme,
            dict_theme={"pop_out": False, "drag_list": True},
        )
        self.button3 = PressTextButton(
            x=200,
            y=200,
            width=150,
            height=30,
            text="imgui button",
            batch=self.main_batch,
            group=self.main_group,
        )
        main_window.push_handlers(self.wiki_button1)
        main_window.push_handlers(self.wiki_button2)
        main_window.push_handlers(self.wiki_button3)
        main_window.push_handlers(self.wiki_button4)
        main_window.push_handlers(self.button3)

    def on_draw(self, dt: float, window: ClientWindow):
        self.main_batch.draw()
