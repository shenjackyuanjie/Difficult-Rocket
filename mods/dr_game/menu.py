#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from pyglet.graphics import Batch, Group

from Difficult_Rocket.client import ClientWindow
from Difficult_Rocket.api.screen import BaseScreen

from Difficult_Rocket.gui.widget.button import OreuiButton

from lib_not_dr import loggers

# from pyglet.text import Label

# from . import DR_mod_runtime
from .render import render_hack_init

logger = loggers.config.get_logger_from_old("client.dr_game_menu", "client")


class Menu(BaseScreen):
    """
    DR game 的 菜单
    """

    name = "DR_game_menu"

    def __init__(self, main_window: ClientWindow):
        super().__init__(main_window)
        self.hacks = None
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

        self.magic_rust_test_button = OreuiButton(
            x=100,
            y=150,
            width=150,
            height=30,
            text="一些魔法 rust 测试",
            toggle_mode=False,
            auto_release=True,
            batch=self.main_batch,
            group=self.main_group,
        )

        def on_release(x, y):
            from .sr1_ship import SR1ShipEditor, SR1ShipSelecter

            main_window.remove_handlers(self.enter_ship_editor_button)
            main_window.remove_handlers(self.magic_rust_test_button)
            main_window.remove_sub_screen("DR_game_menu")
            main_window.add_sub_screen(SR1ShipSelecter.name, SR1ShipSelecter)
            main_window.add_sub_screen(SR1ShipEditor.name, SR1ShipEditor)
            logger.info("added SR1_ship screen", tag="dr_game")

        def render_hacks(x, y):
            from .Difficult_Rocket_rs import render_hack
            if self.hacks is not None:
                return
            render = render_hack()
            if render is not None:
                self.hacks = render
                logger.info("render_hack_init", tag="dr_game_hacks")


        self.enter_ship_editor_button.set_handler("on_release", on_release)
        self.magic_rust_test_button.set_handler("on_release", render_hacks)
        main_window.push_handlers(self.enter_ship_editor_button)
        main_window.push_handlers(self.magic_rust_test_button)

    def on_draw(self, window: ClientWindow):
        self.main_batch.draw()
