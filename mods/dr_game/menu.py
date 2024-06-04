#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from typing import Optional, Tuple
from pyglet.graphics import Batch, Group

from Difficult_Rocket.client import ClientWindow
from Difficult_Rocket.api.screen import BaseScreen
from Difficult_Rocket.main import Game
from Difficult_Rocket.gui.widget.button import (
    PressTextButton,
    MinecraftWikiButtonTheme,
    ButtonThemeOptions,
    BaseButtonTheme,
)

from lib_not_dr import loggers

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
        self.enter_ship_editor_button = PressTextButton(
            x=100,
            y=100,
            width=150,
            height=30,
            text="进入编辑器",
            batch=self.main_batch,
            group=self.main_group,
            draw_theme=MinecraftWikiButtonTheme,
            dict_theme={"pop_out": True}
        )

        def on_release(button: PressTextButton, x, y):
            logger.info("on_mouse_release", x, y, button, tag="dr_game")
            from .sr1_ship import SR1ShipRender
            main_window.remove_sub_screen("DR_game_menu")
            main_window.add_sub_screen("SR1_ship", SR1ShipRender)
            logger.info("added SR1_ship screen", tag="dr_game")

        self.enter_ship_editor_button.set_handler("on_release", on_release)
        # main_window.push_handlers(self.wiki_button1)
        # main_window.push_handlers(self.wiki_button2)
        # main_window.push_handlers(self.wiki_button3)
        # main_window.push_handlers(self.wiki_button4)
        # main_window.push_handlers(self.button3)
        main_window.push_handlers(self.enter_ship_editor_button)

    def on_draw(self, dt: float, window: ClientWindow):
        self.main_batch.draw()


# class PressEnterShipEditorButton(PressTextButton):
#     def __init__(
#         self,
#         window: ClientWindow,
#         x: int,
#         y: int,
#         width: int,
#         height: int,
#         text: str,
#         batch: Optional[Batch] = None,
#         group: Optional[Group] = None,
#         theme: Optional[ButtonThemeOptions] = None,
#         draw_theme: Optional[BaseButtonTheme] = None,
#         dict_theme: Optional[dict] = None,
#     ):
#         super().__init__(
#             x, y, width, height, text, batch, group, theme, draw_theme, dict_theme
#         )
#         self.window = window


#     def on_mouse_release(self, x, y, buttons, modifiers):
#         if self.pressed and (x, y) in self:
#             if self.draw_theme:
#                 self.draw_theme.on_disable(self)
#             else:
#                 self.back_rec.color = self.touched_color
#             self.pressed = False

#             from .sr1_ship import SR1ShipRender

#             self.window.remove_sub_screen("DR_game_menu")
#             self.window.add_sub_screen("SR1_ship", SR1ShipRender)
#             logger.info("added SR1_ship screen", tag="dr_game")
