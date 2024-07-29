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
    PressTextButton,
    MinecraftWikiButtonTheme,
    WikiButton,
    WikiButtonShape,
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

        # self.wiki_button1 = PressTextButton(
        #     x=200,
        #     y=300,
        #     width=150,
        #     height=30,
        #     text="wiki button1",
        #     batch=self.main_batch,
        #     group=self.main_group,
        #     draw_theme=MinecraftWikiButtonTheme,
        #     dict_theme={"pop_out": True},
        # )
        # self.wiki_button2 = PressTextButton(
        #     x=400,
        #     y=300,
        #     width=150,
        #     height=30,
        #     text="wiki button2",
        #     batch=self.main_batch,
        #     group=self.main_group,
        #     draw_theme=MinecraftWikiButtonTheme,
        #     dict_theme={"pop_out": False},
        # )
        # self.wiki_button3 = PressTextButton(
        #     x=200,
        #     y=250,
        #     width=150,
        #     height=30,
        #     text="wiki button3",
        #     batch=self.main_batch,
        #     group=self.main_group,
        #     draw_theme=MinecraftWikiButtonTheme,
        #     dict_theme={"pop_out": True, "drag_list": True},
        # )
        # self.wiki_button4 = PressTextButton(
        #     x=400,
        #     y=250,
        #     width=150,
        #     height=30,
        #     text="wiki button4",
        #     batch=self.main_batch,
        #     group=self.main_group,
        #     draw_theme=MinecraftWikiButtonTheme,
        #     dict_theme={"pop_out": False, "drag_list": True},
        # )
        # self.button3 = PressTextButton(
        #     x=200,
        #     y=200,
        #     width=150,
        #     height=30,
        #     text="imgui button",
        #     batch=self.main_batch,
        #     group=self.main_group,
        # )

        # 16、20、24、32、40、48 64
        # self.test_label = Label(
        #     x=20, y=200,
        #     font_name="Segoe Fluent Icons",
        #     font_size=32,
        #     text="\uE003 \uE005 \uE0A2
        # \uE88B \uE88C \uE88D \uE985 \uE97E \uF7B5
        # \uE971 \uE972 \uE973 \uE974",
        #     batch=self.main_batch,
        #     group=self.main_group,
        # )

        self.enter_ship_editor_button = PressTextButton(
            x=100,
            y=100,
            width=150,
            height=30,
            text="进入编辑器",
            batch=self.main_batch,
            group=self.main_group,
            draw_theme=MinecraftWikiButtonTheme,
            dict_theme={"pop_out": True},
        )

        self.tester = WikiButton(
            x=100,
            y=150,
            width=150,
            height=30,
            batch=self.main_batch,
            group=self.main_group,
        )

        self.wiki_shape1 = WikiButtonShape(
            x=100,
            y=200,
            width=150,
            height=100,
            pad=10,
            down_pad=15,
            batch=self.main_batch,
            group=self.main_group,
        )
        self.wiki_shape2 = WikiButtonShape(
            x=300,
            y=200,
            pop_out=False,
            width=150,
            height=100,
            pad=2,
            down_pad=5,
            batch=self.main_batch,
            group=self.main_group,
        )

        def on_release(button: PressTextButton, x, y):
            ...
            # self.tester.clockwise = not self.tester.clockwise
            # from .sr1_ship import SR1ShipEditor
            # main_window.remove_sub_screen("DR_game_menu")
            # main_window.add_sub_screen("SR1_ship", SR1ShipEditor)
            # logger.info("added SR1_ship screen", tag="dr_game")

        self.enter_ship_editor_button.set_handler("on_release", on_release)
        # main_window.push_handlers(self.wiki_button1)
        # main_window.push_handlers(self.wiki_button2)
        # main_window.push_handlers(self.wiki_button3)
        # main_window.push_handlers(self.wiki_button4)
        # main_window.push_handlers(self.button3)
        main_window.push_handlers(self.enter_ship_editor_button)

    def on_mouse_press(
        self, x: int, y: int, button: int, modifiers: int, window: ClientWindow
    ):
        if (x, y) in self.wiki_shape1:
            self.wiki_shape1.pop_out = not self.wiki_shape1.pop_out
        if (x, y) in self.wiki_shape2:
            self.wiki_shape2.pop_out = not self.wiki_shape2.pop_out

    # def on_draw(self, dt: float, window: ClientWindow): # TODO: wait for pyglet 2.1
    def on_draw(self, window: ClientWindow):
        self.main_batch.draw()
