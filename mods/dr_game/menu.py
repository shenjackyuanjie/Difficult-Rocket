#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import random

from pyglet.graphics import Batch, Group

from Difficult_Rocket.client import ClientWindow
from Difficult_Rocket.api.screen import BaseScreen

from Difficult_Rocket.gui.widget.button import OreuiButton

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
        self.wgpu_hacks = None
        self.gl_hacks = None
        self.enable_hacks = True
        self.main_batch = Batch()
        self.main_group = Group(parent=main_window.main_group, order=1)

        # 占位, 高二看看能不能咕出来点啥 (20230911)
        # 欸呀, 正好是 911 纪念日哦
        # 好, 高二 第一学期 期末都考完了, 我过来做测试了 (20240119)
        # 高二, 马上要研学了, 似乎做了点啥, 但似乎又没做点啥 (20240526)
        # 高二最后一个暑假都过了一半了, 可算把按钮好歹写完了 (20240804)
        # 高三二模第二天, 我回来写点 opengl 了 (20250507)
        # 高考第三天, 我来写点 taskbar (20250609)

        self.enter_ship_editor_button = OreuiButton(
            x=100,
            y=100,
            width=200,
            height=30,
            text="进入编辑器aaaa",
            toggle_mode=False,
            auto_release=True,
            batch=self.main_batch,
            group=self.main_group,
        )

        self.magic_rust_wgpu_test_button = OreuiButton(
            x=100,
            y=150,
            width=200,
            height=30,
            text="一些魔法 rust 测试 (wgpu)",
            toggle_mode=False,
            auto_release=True,
            batch=self.main_batch,
            group=self.main_group,
        )

        self.magic_rust_gl_test_button = OreuiButton(
            x=100,
            y=200,
            width=200,
            height=30,
            text="一些魔法 rust 测试 (opengl)",
            toggle_mode=False,
            auto_release=True,
            batch=self.main_batch,
            group=self.main_group,
        )

        self.task_bar_test_button = OreuiButton(
            x=100,
            y=250,
            width=200,
            height=30,
            text="一些控制栏测试",
            toggle_mode=False,
            auto_release=True,
            batch=self.main_batch,
            group=self.main_group,
        )

        def on_release(x, y):
            from .sr1_ship import SR1ShipEditor, SR1ShipSelecter

            main_window.remove_handlers(self.enter_ship_editor_button)
            main_window.remove_handlers(self.magic_rust_wgpu_test_button)
            main_window.remove_handlers(self.magic_rust_gl_test_button)
            main_window.remove_sub_screen("DR_game_menu")
            main_window.add_sub_screen(SR1ShipSelecter.name, SR1ShipSelecter)
            main_window.add_sub_screen(SR1ShipEditor.name, SR1ShipEditor)
            logger.info("added SR1_ship screen", tag="dr_game")

        def render_hacks_wgpu(x, y):
            from .Difficult_Rocket_rs import render_hack
            if self.wgpu_hacks is not None:
                logger.info("render_hack 已经做过了", tag="dr_game_wgpu_hacks")
                return
            render = render_hack()
            if render is not None:
                render.on_resize(main_window.width, main_window.height)
                self.wgpu_hacks = render
                logger.info("render_hack_inited", tag="dr_game_wgpu_hacks")


        def render_hacks_gl(x, y):
            from .Difficult_Rocket_rs import opengl_render
            if self.gl_hacks is not None:
                logger.info("render_hack 已经做过了", tag="dr_game_gl_hacks")
                return
            render = opengl_render(main_window.width, main_window.height)
            if render is not None:
                self.gl_hacks = render
                logger.info("render_hack_inited", tag="dr_game_gl_hacks")


        def taks_bar_test(x, y):
            from .Difficult_Rocket_rs import set_progress_value
            full = 1000
            complete = random.randint(1, 1000)
            logger.info(f"将把任务栏进度条设置为 {full}/{complete}")
            set_progress_value(full, complete)

        self.enter_ship_editor_button.set_handler("on_release", on_release)
        self.magic_rust_wgpu_test_button.set_handler("on_release", render_hacks_wgpu)
        self.magic_rust_gl_test_button.set_handler("on_release", render_hacks_gl)
        self.task_bar_test_button.set_handler("on_release", taks_bar_test)
        main_window.push_handlers(self.enter_ship_editor_button)
        main_window.push_handlers(self.magic_rust_wgpu_test_button)
        main_window.push_handlers(self.magic_rust_gl_test_button)
        main_window.push_handlers(self.task_bar_test_button)

    def on_resize(self, width, height, window: ClientWindow):
        if self.wgpu_hacks is not None:
            self.wgpu_hacks.on_resize(width, height)
        if self.gl_hacks is not None:
            self.gl_hacks.on_resize(width, height)

    def on_mouse_press(self, x, y, button, modifiers, window):
        if button == 1:
            self.enable_hacks = not self.enable_hacks
            logger.info(f"enable_hacks: {self.enable_hacks}", tag="dr_game_hacks")

    def on_draw(self, window: ClientWindow):
        self.main_batch.draw()
        if self.wgpu_hacks is not None:
            self.wgpu_hacks.on_draw(not self.enable_hacks)
        if self.gl_hacks is not None:
            self.gl_hacks.on_draw()
