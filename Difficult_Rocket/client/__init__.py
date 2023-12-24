#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
import sys
import time
import inspect
import functools
import traceback

from pathlib import Path
from decimal import Decimal
from typing import Callable, Dict, List, TYPE_CHECKING, Type

# third function
import rtoml
import pyglet

# from pyglet import gl
# from pyglet.gl import glClearColor
# from pyglet.libs.win32 import _user32
from pyglet.graphics import Group, Batch
from pyglet.window import Window
from pyglet.window import key, mouse
from pyglet.gui.widgets import TextEntry

# Difficult_Rocket function
if TYPE_CHECKING:
    from Difficult_Rocket.main import Game
from Difficult_Rocket import DR_status
from Difficult_Rocket.utils import tools
from Difficult_Rocket.command import line
from Difficult_Rocket.api.types import Options
from Difficult_Rocket.utils.translate import tr
from Difficult_Rocket.runtime import DR_runtime
from Difficult_Rocket.api.screen import BaseScreen
from Difficult_Rocket.utils.thread import new_thread
from Difficult_Rocket.client.screen import DRDEBUGScreen
from Difficult_Rocket.client.fps.fps_log import FpsLogger
from Difficult_Rocket.exception.language import LanguageNotFound

from lib_not_dr import loggers

logger = loggers.config.get_logger("client")


class ClientOption(Options):
    fps: int = 60
    width: int = 1024
    height: int = 768
    file_drop: bool = True
    fullscreen: bool = False
    resizeable: bool = True
    visible: bool = True
    gui_scale: float = 1.0
    vsync: bool = False
    background_color: List[float] = [21 / 255, 22 / 255, 23 / 255, 0.0]
    caption: str = "Difficult Rocket v{DR_version}"

    def load_file(self) -> None:
        file = DR_runtime.main_config
        self.fps = int(file["runtime"]["fps"])
        self.width = int(file["window"]["width"])
        self.height = int(file["window"]["height"])
        self.fullscreen = tools.format_bool(file["window"]["full_screen"])
        self.resizeable = tools.format_bool(file["window"]["resizable"])
        self.gui_scale = float(file["window"]["gui_scale"])
        self.caption = DR_status.format(file["window"]["caption"])
        self.vsync = tools.format_bool(file["window"]["vsync"])
        color = (i / 255 for i in file["window"]["background_color"][0:3])
        alpha = file["window"]["background_color"][3]
        self.background_color = [*color, alpha]
        self.caption = DR_runtime.format(self.caption)


class Client:
    """
    客户端
    """

    def __init__(self, game: "Game", net_mode="local"):
        start_time = time.time_ns()
        # log
        self.logger = loggers.get_logger("client").set_tag("client")
        self.logger.info(tr().client.setup.start())
        # config
        self.config = ClientOption()
        # value
        self.process_id = "Client"
        self.process_name = "Client process"
        self.process_pid = os.getpid()
        self.net_mode = net_mode
        self.game = game
        self.window = ClientWindow(
            game=game,
            net_mode=self.net_mode,
            width=self.config.width,
            height=self.config.height,
            fullscreen=self.config.fullscreen,
            caption=self.config.caption,
            resizable=self.config.resizeable,
            visible=self.config.visible,
            file_drops=True,
            vsync=False,
        )
        pyglet.gl.glClearColor(*self.config.background_color)
        end_time = time.time_ns()
        self.use_time = end_time - start_time
        self.logger.info(
            tr().client.setup.use_time().format(Decimal(self.use_time) / 1000000000)
        )
        self.logger.debug(tr().client.setup.use_time_ns().format(self.use_time))

    def start(self):
        """
        启动客户端
        """
        DR_runtime.running = True
        self.window.start_game()  # 游戏启动
        # TODO 写一下服务端启动相关，还是需要服务端啊

    def __repr__(self):
        return f"<Client {self.process_name} {self.process_pid}>"


def pyglet_load_fonts_folder(folder) -> None:
    """
    递归加载字体文件夹
    :param folder:
    :return:
    """
    font_path = Path(folder)
    if not font_path.exists():
        font_path.mkdir(parents=True)
        return None
    logger.info(tr().client.load.font.start().format(font_path), tag="font")
    start_time = time.time_ns()
    for dir_path, dir_names, file_names in os.walk(font_path):
        dir_path = Path(dir_path)
        for file_name in file_names:
            file_name = Path(file_name)
            if file_name.suffix in (".ttf", ".otf"):
                logger.debug(
                    tr().client.load.font.file().format(str(dir_path / file_name)),
                    tag="font",
                )
                try:
                    pyglet.font.add_file(str(dir_path / file_name))
                except Exception:
                    logger.error(
                        tr()
                        .client.load.font.error()
                        .format(str(dir_path / file_name), traceback.format_exc())
                    )
    end_time = time.time_ns()
    use_time = end_time - start_time
    logger.info(
        tr().client.load.font.use_time().format(use_time / 1000000000), tag="font"
    )


def _call_back(call_back: Callable) -> Callable:
    """
    >>> def call_back_example():
    >>>     pass
    >>> @_call_back(call_back_example)
    >>> def on_draw(self):
    >>>     pass
    用于在调用窗口函数后调用指定函数 的装饰器
    :param call_back: 需要调用的函数
    :return: 包装后的函数
    """

    def wrapper(func):
        @functools.wraps(func)
        def warp(self: "ClientWindow", *args, **kwargs):
            result = func(self, *args, **kwargs)
            # call_back(self)
            return result

        return warp

    return wrapper


def _call_screen_after(func: Callable) -> Callable:
    """
    >>> @_call_screen_after
    >>> def on_draw(self):
    >>>     pass
    用于在调用窗口函数后调用子窗口函数 的装饰器
    :param func: 需要包装的函数
    :return: 包装后的函数
    """

    @functools.wraps(func)
    def warped(self: "ClientWindow", *args, **kwargs):
        result = func(self, *args, **kwargs)
        for title, a_screen in self.screen_list.items():
            a_screen.window_pointer = self
            # 提前帮子窗口设置好指针
            if hasattr(a_screen, func.__name__):
                try:
                    getattr(a_screen, func.__name__)(*args, **kwargs, window=self)
                except Exception:
                    traceback.print_exc()
        return result

    warped.__signature__ = inspect.signature(func) # type: ignore
    return warped


def _call_screen_before(func: Callable) -> Callable:
    """
    >>> @_call_screen_before
    >>> def on_draw(self):
    >>>     pass
    用于在调用窗口函数前调用子窗口函数 的装饰器
    :param func: 需要包装的函数
    :return: 包装后的函数
    """

    @functools.wraps(func)
    def warped(self: "ClientWindow", *args, **kwargs):
        for title, a_screen in self.screen_list.items():
            a_screen.window_pointer = self
            # 提前帮子窗口设置好指针
            if hasattr(a_screen, func.__name__):
                try:
                    getattr(a_screen, func.__name__)(*args, **kwargs, window=self)
                except Exception:
                    traceback.print_exc()
        result = func(self, *args, **kwargs)
        return result

    warped.__signature__ = inspect.signature(func) # type: ignore
    return warped


class ClientWindow(Window):
    def __init__(self, game: "Game", net_mode="local", *args, **kwargs):
        """

        @param net_mode:
        @param args:
        @param kwargs:
        """
        start_time = time.time_ns()
        super().__init__(*args, **kwargs)
        # log
        self.logger = loggers.get_logger("client").set_tag("window")
        self.logger.info(tr().window.setup.start())
        # value
        self.game = game
        self.net_mode = net_mode
        self.run_input = False
        self.command_list: List[str] = []
        # FPS
        self.FPS = Decimal(int(DR_runtime.main_config["runtime"]["fps"]))
        self.SPF = Decimal("1") / self.FPS
        self.fps_log = FpsLogger(stable_fps=int(self.FPS))
        # batch
        self.main_batch = Batch()
        self.main_group = Group(0)
        # frame
        self.frame = pyglet.gui.Frame(self, order=20)
        self.M_frame = pyglet.gui.MovableFrame(self, modifier=key.LCTRL)
        self.screen_list: Dict[str, BaseScreen] = {}
        # setup
        self.setup()
        # 命令显示
        self.input_box = TextEntry(
            x=50,
            y=30,
            width=300,
            batch=self.main_batch,
            text="",
            group=Group(1000, parent=self.main_group),
        )  # 实例化
        self.input_box.push_handlers(self)
        self.input_box.set_handler("on_commit", self.on_input)
        self.push_handlers(self.input_box)
        self.input_box.enabled = True
        # 设置刷新率
        # pyglet.clock.schedule_interval(self.draw_update, float(self.SPF))
        # 完成设置后的信息输出
        self.logger.info(tr().window.os.pid_is().format(os.getpid(), os.getppid()))
        end_time = time.time_ns()
        self.use_time = end_time - start_time
        DR_runtime.client_setup_cause_ns = self.use_time
        self.logger.info(tr().window.setup.use_time().format(self.use_time / 1000000000))
        self.logger.debug(tr().window.setup.use_time_ns().format(self.use_time))

    def setup(self):
        self.set_icon(pyglet.image.load("assets/textures/icon.png"))
        self.load_fonts()
        self.screen_list["DR_debug"] = DRDEBUGScreen(self)
        self.game.dispatch_mod_event("on_client_start", game=self.game, client=self)

    def load_fonts(self) -> None:
        fonts_folder_path = DR_runtime.main_config["runtime"]["fonts_folder"]
        # 加载字体路径
        # 淦，还写了个递归来处理
        pyglet_load_fonts_folder(fonts_folder_path)

    def start_game(self) -> None:
        self.set_icon(pyglet.image.load("assets/textures/icon.png"))
        try:
            pyglet.clock.schedule_interval(self.draw_call, float(self.SPF))
            pyglet.app.run(None)
        except KeyboardInterrupt:
            self.logger.warn(
                "==========client stop. KeyboardInterrupt info==========", tag="starter"
            )
            traceback.print_exc()
            self.logger.warn(
                "==========client stop. KeyboardInterrupt info end==========",
                tag="starter",
            )
            self.dispatch_event("on_close", "input")
            sys.exit(0)

    @new_thread("window save_info")
    def save_info(self):
        self.logger.info(tr().client.config.save.start())
        config_file = DR_runtime.main_config
        config_file["window"]["width"] = self.width
        config_file["window"]["height"] = self.height
        config_file["runtime"]["language"] = DR_runtime.language
        rtoml.dump(config_file, open("./config/main.toml", "w"))
        self.logger.info(tr().client.config.save.done())

    """
    client api
    """

    def add_sub_screen(self, title: str, sub_screen: Type[BaseScreen]):
        self.screen_list[title] = sub_screen(self)

    def remove_sub_screen(self, title: str):
        self.screen_list.pop(title)

    """
    draws and some event
    """

    @_call_screen_after
    def draw_update(self, tick: float):
        decimal_tick = Decimal(str(tick)[:10])
        now_FPS = pyglet.clock.get_frequency()
        self.fps_log.update_tick(now_FPS, decimal_tick)

    def draw_call(self, dt: float):
        self.switch_to()
        # self.logger.debug(f"draw call {dt}")
        self.on_draw(dt)
        self.flip()

    @_call_screen_after
    def on_draw(self, dt: float):
        while (command := self.game.console.get_command()) is not None:
            self.on_command(line.CommandText(command))
        self.clear()
        self.draw_update(dt)
        self.draw_batch()

    @_call_screen_after
    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)

    @_call_screen_after
    def on_refresh(self, dt):
        ...

    @_call_screen_after
    def on_show(self):
        # HWND_TOPMOST = -1
        # _user32.SetWindowPos(self._hwnd, HWND_TOPMOST, 0, 0, self.width, self.height, 0)
        ...

    @_call_screen_after
    def on_hide(self):
        # self.set_location(*self.get_location())
        print("on hide!")

    @_call_screen_before
    def draw_batch(self):
        self.main_batch.draw()

    """
    command line event
    """

    def on_input(self, message: str) -> None:
        command_text = line.CommandText(message)
        self.on_command(command_text)
        self.input_box.value = ""

    def new_command(self):
        self.game.console.new_command()

    @_call_back(new_command)
    @_call_screen_after
    def on_command(self, command: line.CommandText):
        command.text = command.text.rstrip("\n").rstrip(" ").strip("/")
        self.logger.info(tr().window.command.text().format(f"|{command.text}|"))
        if command.find("stop"):
            self.logger.info("command stop!")
            # HUGE THANKS to Discord @nokiyasos for this fix!
            pyglet.app.exit()
        elif command.find("fps"):
            if command.find("log"):
                self.logger.debug(self.fps_log.fps_list)
            elif command.find("max"):
                self.logger.info(self.fps_log.max_fps)
                # self.command.push_line(self.fps_log.max_fps, block_line=True)
            elif command.find("min"):
                self.logger.info(self.fps_log.min_fps)
                # self.command.push_line(self.fps_log.min_fps, block_line=True)
        elif command.find("default"):
            self.set_size(
                int(DR_runtime.main_config["window_default"]["width"]),
                int(DR_runtime.main_config["window_default"]["height"]),
            )
        elif command.find("lang"):
            try:
                lang = command.text[5:]
                tr._language = lang
                self.logger.info(tr().language_set_to())
            except LanguageNotFound:
                self.logger.info(
                    tr().language_available().format(os.listdir("./config/lang")), tag="command"
                )
            self.save_info()
        elif command.find("mods"):
            if command.find("list"):
                self.logger.info(tr().mod.list())
                for mod in self.game.mod_manager.loaded_mod_modules.values():
                    self.logger.info(
                        f"mod: {mod.name} id: {mod.mod_id} version: {mod.version}", tag="command"
                    )
            elif command.find("reload"):
                if not len(command.text) == 0:
                    print(f"reload mod: |{command.text}|")
                    self.game.mod_manager.reload_mod(command.text, game=self.game)
                else:
                    self.logger.info(tr().window.command.mods.reload.no_mod_id(), tag="command")

    @_call_screen_after
    def on_message(self, message: line.CommandText):
        self.logger.info(tr().window.message.text().format(message), tag="message")

    """
    keyboard and mouse input
    """

    @_call_screen_after
    def on_activate(self):
        super().activate()

    @_call_screen_after
    def on_deactivate(self):
        ...

    @_call_screen_before
    def on_move(self, x, y):
        ...

    @_call_screen_after
    def on_mouse_motion(self, x, y, dx, dy):
        ...

    @_call_screen_after
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        ...

    @_call_screen_after
    def on_mouse_enter(self, x, y):
        ...

    @_call_screen_after
    def on_mouse_leave(self, x, y):
        ...

    @_call_screen_after
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers) -> None:
        ...

    @_call_screen_after
    def on_mouse_press(self, x, y, button, modifiers) -> None:
        self.logger.debug(
            tr()
            .window.mouse.press()
            .format([x, y], tr().window.mouse[mouse.buttons_string(button)]()), tag="mouse"
        )

    @_call_screen_after
    def on_mouse_release(self, x, y, button, modifiers) -> None:
        self.logger.debug(
            tr()
            .window.mouse.release()
            .format([x, y], tr().window.mouse[mouse.buttons_string(button)]()), tag="mouse"
        )

    @_call_screen_after
    def on_key_press(self, symbol, modifiers) -> None:
        if symbol == key.ESCAPE and not (
                modifiers & ~(key.MOD_NUMLOCK | key.MOD_CAPSLOCK | key.MOD_SCROLLLOCK)
        ):
            self.dispatch_event("on_close", "window")
        if symbol == key.SLASH:
            self.input_box._set_focus(True)
        self.logger.debug(
            tr()
            .window.key.press()
            .format(key.symbol_string(symbol), key.modifiers_string(modifiers)), tag="key"
        )

    @_call_screen_after
    def on_key_release(self, symbol, modifiers) -> None:
        self.logger.debug(
            tr()
            .window.key.release()
            .format(key.symbol_string(symbol), key.modifiers_string(modifiers)), tag="key"
        )

    @_call_screen_after
    def on_file_drop(self, x, y, paths):
        ...

    @_call_screen_after
    def on_text(self, text):
        if text == "\r":
            self.logger.debug(tr().window.text.new_line(), tag="text")
        else:
            self.logger.debug(tr().window.text.input().format(text), tag="text")
            if text == "t":
                self.input_box.enabled = True

    @_call_screen_after
    def on_text_motion(self, motion):
        motion_string = key.motion_string(motion)
        self.logger.debug(tr().window.text.motion().format(motion_string), tag="text")

    @_call_screen_after
    def on_text_motion_select(self, motion):
        motion_string = key.motion_string(motion)
        self.logger.debug(tr().window.text.motion_select().format(motion_string), tag="text")

    @_call_screen_before
    def on_close(self, source: str = "window") -> None:
        self.game.dispatch_mod_event(
            "on_close", game=self.game, client=self, source=source
        )
        self.logger.info(tr().window.game.stop_get().format(tr().game[source]()), tag="window")
        self.logger.info(tr().window.game.stop(), tag="window")
        # self.fps_log.check_list = False
        DR_runtime.running = False
        if self.run_input:
            self.run_input = False
        self.save_info()
        super().on_close()
        self.logger.info(tr().window.game.end(), tag="window")


ClientWindow.register_event_type("on_command")
