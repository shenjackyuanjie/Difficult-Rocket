#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""
import inspect
# system function
import os
import time
import logging
import functools
import traceback

from typing import List, Callable, Union
from decimal import Decimal

# third function
import rtoml
import pyglet
# from pyglet import gl
# from pyglet.gl import glClearColor
# from pyglet.libs.win32 import _user32
from pyglet.window import Window
from pyglet.window import key, mouse

# Difficult_Rocket function
from Difficult_Rocket.api.types import Options
from Difficult_Rocket.command import line, tree
from Difficult_Rocket.utils.translate import tr
from Difficult_Rocket import DR_runtime, DR_option
from Difficult_Rocket.utils import tools, translate
from Difficult_Rocket.utils.new_thread import new_thread
from Difficult_Rocket.client.fps.fps_log import FpsLogger
from Difficult_Rocket.client.guis.widgets import InputBox
from Difficult_Rocket.exception.command import CommandError
from Difficult_Rocket.client.render.sr1_ship import SR1ShipRender
from Difficult_Rocket.client.screen import BaseScreen, DRScreen, DRDEBUGScreen


class ClientOption(Options):
    fps: int = 60
    width: int = 1024
    height: int = 768
    file_drop: bool = True
    fullscreen: bool = False
    resizeable: bool = True
    visible: bool = True
    gui_scale: float = 1.0
    caption: str = "Difficult Rocket v{DR_version}|DR_rs v{DR_Rust_get_version}"

    def load_file(self) -> None:
        file = tools.load_file('./configs/main.toml')
        self.fps = file['runtime']['fps']
        self.width = file['window']['width']
        self.height = file['window']['height']
        self.resizeable = file['window']['resizable']
        self.fullscreen = file['window']['full_screen']


class Client:
    def __init__(self, net_mode='local'):
        start_time = time.time_ns()
        # logging
        self.logger = logging.getLogger('client')
        # config
        self.config = tools.load_file('./configs/main.toml')
        # value
        self.process_id = 'Client'
        self.process_name = 'Client process'
        self.process_pid = os.getpid()
        self.net_mode = net_mode
        self.caption = DR_runtime.format(self.config['window']['caption'])
        file_drop = bool(
            pyglet.compat_platform != 'darwin' or DR_option.pyglet_macosx_dev_test
        )
        self.window = ClientWindow(net_mode=self.net_mode,
                                   width=int(self.config['window']['width']),
                                   height=int(self.config['window']['height']),
                                   fullscreen=tools.format_bool(self.config['window']['full_screen']),
                                   caption=self.caption,
                                   resizable=tools.format_bool(self.config['window']['resizable']),
                                   visible=tools.format_bool(self.config['window']['visible']),
                                   file_drops=file_drop)
        self.logger.info(tr.lang('client', 'setup.done'))
        end_time = time.time_ns()
        self.use_time = end_time - start_time
        self.logger.info(tr.lang('client', 'setup.use_time').format(Decimal(self.use_time) / 1000000000))
        self.logger.debug(tr.lang('client', 'setup.use_time_ns').format(self.use_time))

    def start(self):
        DR_runtime.running = True
        self.window.start_game()  # 游戏启动
        # TODO 写一下服务端启动相关，还是需要服务端啊


def pyglet_load_fonts_folder(folder) -> None:
    file_folder_list = os.listdir(folder)
    for obj in file_folder_list:
        if os.path.isfile(os.path.join(folder, obj)):
            if obj[-4:] == '.ttf':
                pyglet.font.add_file(os.path.join(folder, obj))
        else:
            pyglet_load_fonts_folder(os.path.join(folder, obj))


def _call_screen_after(func: Callable) -> Callable:
    @functools.wraps(func)
    def warped(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        for a_screen in self.screen_list:
            if hasattr(a_screen, func.__name__):
                try:
                    getattr(a_screen, func.__name__)(*args, **kwargs)
                except Exception:
                    traceback.print_exc()
        return result

    warped.__signature__ = inspect.signature(func)
    return warped


def _call_screen_before(func: Callable) -> Callable:
    @functools.wraps(func)
    def warped(self, *args, **kwargs):
        for a_screen in self.screen_list:
            if hasattr(a_screen, func.__name__):
                try:
                    getattr(a_screen, func.__name__)(*args, **kwargs)
                except Exception:
                    traceback.print_exc()
        result = func(self, *args, **kwargs)
        return result

    warped.__signature__ = inspect.signature(func)
    return warped


class ClientWindow(Window):

    def __init__(self, net_mode='local', *args, **kwargs):
        """

        @param net_mode:
        @param args:
        @param kwargs:
        """
        start_time = time.time_ns()
        super().__init__(*args, **kwargs)
        # logging
        self.logger = logging.getLogger('client')
        # value
        self.net_mode = net_mode
        self.run_input = False
        # configs
        self.set_icon(pyglet.image.load('./textures/icon.png'))
        self.main_config = tools.load_file('./configs/main.toml')
        self.game_config = tools.load_file('./configs/game.config')
        # FPS
        self.FPS = Decimal(int(self.main_config['runtime']['fps']))
        self.SPF = Decimal('1') / self.FPS
        self.fps_log = FpsLogger(stable_fps=int(self.FPS))
        # batch
        self.part_batch = pyglet.graphics.Batch()
        self.label_batch = pyglet.graphics.Batch()
        # frame
        self.frame = pyglet.gui.Frame(self, order=20)
        self.M_frame = pyglet.gui.MovableFrame(self, modifier=key.LCTRL)
        self.screen_list = []
        # setup
        self.setup()
        # 命令显示
        self.command_group = pyglet.graphics.Group(0)
        self.command_tree = tree.CommandTree(tree.DR_command)
        self.input_box = InputBox(x=50, y=30, width=300,
                                  batch=self.label_batch, text='')  # 实例化
        self.input_box.push_handlers(self)
        self.input_box.set_handler('on_commit', self.on_input)
        self.push_handlers(self.input_box)
        self.input_box.enabled = True
        # 设置刷新率
        pyglet.clock.schedule_interval(self.draw_update, float(self.SPF))
        # 完成设置后的信息输出
        self.logger.info(tr.lang('window', 'setup.done'))
        self.logger.info(tr.lang('window', 'os.pid_is').format(os.getpid(), os.getppid()))
        end_time = time.time_ns()
        self.use_time = end_time - start_time
        DR_runtime.client_setup_cause_ns = self.use_time
        self.logger.info(tr.lang('window', 'setup.use_time').format(Decimal(self.use_time) / 1000000000))
        self.logger.debug(tr.lang('window', 'setup.use_time_ns').format(self.use_time))
        self.count = 0

    def setup(self):
        self.load_fonts()
        self.screen_list: List[BaseScreen]
        self.screen_list.append(DRDEBUGScreen(self))
        self.screen_list.append(DRScreen(self))
        self.screen_list.append(SR1ShipRender(self, DR_option.gui_scale))

    def load_fonts(self) -> None:
        fonts_folder_path = self.main_config['runtime']['fonts_folder']
        # 加载字体路径
        # 淦，还写了个递归来处理
        pyglet_load_fonts_folder(fonts_folder_path)

    # @new_thread('window load_editor')
    def load_editor(self):
        pass

    def start_game(self) -> None:
        self.run_input = True
        self.read_input()
        pyglet.app.event_loop.run(1 / self.main_config['runtime']['fps'])

    @new_thread('window read_input', daemon=True)
    def read_input(self):
        self.logger.debug('read_input start')
        while self.run_input:
            get = input()
            if get in ('', ' ', '\n', '\r'):
                continue
            if get == 'stop':
                self.run_input = False
            try:
                self.on_command(line.CommandText(get))
            except CommandError:
                self.logger.error(traceback.format_exc())
        self.logger.debug('read_input end')

    @new_thread('window save_info')
    def save_info(self):
        self.logger.info('save_info start')
        config_file = tools.load_file('./configs/main.toml')
        config_file['window']['width'] = self.width
        config_file['window']['height'] = self.height
        rtoml.dump(config_file, open('./configs/main.toml', 'w'))
        self.logger.info('save_info end')

    """
    draws and some event
    """

    @_call_screen_after
    def draw_update(self, tick: float):
        decimal_tick = Decimal(str(tick)[:10])
        now_FPS = pyglet.clock.get_frequency()
        self.fps_log.update_tick(now_FPS, decimal_tick)

    @_call_screen_after
    def on_draw(self, *dt):
        # self.logger.debug('on_draw call dt: {}'.format(dt))
        pyglet.gl.glClearColor(0.1, 0, 0, 0.0)
        self.clear()
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
        print('on hide!')

    @_call_screen_after
    def draw_batch(self):
        self.part_batch.draw()
        self.label_batch.draw()

    """
    command line event
    """

    def on_input(self, message: str) -> None:
        command_text = line.CommandText(message)
        self.on_command(command_text)
        self.input_box.value = ''

    @_call_screen_after
    def on_command(self, command: line.CommandText):
        self.logger.info(tr.lang('window', 'command.text').format(command))
        if command.re_match('stop'):
            # self.dispatch_event('on_exit')
            pyglet.app.platform_event_loop.stop()
            self.dispatch_event('on_close', 'command')  # source = command
        elif command.re_match('fps'):
            if command.re_match('log'):
                self.logger.debug(self.fps_log.fps_list)
            elif command.re_match('max'):
                self.logger.info(self.fps_log.max_fps)
                self.command.push_line(self.fps_log.max_fps, block_line=True)
            elif command.re_match('min'):
                self.logger.info(self.fps_log.min_fps)
                self.command.push_line(self.fps_log.min_fps, block_line=True)
        elif command.re_match('default'):
            self.set_size(int(self.main_config['window_default']['width']),
                          int(self.main_config['window_default']['height']))
        # self.command_tree.parse(command.plain_command)

    @_call_screen_after
    def on_message(self, message: line.CommandLine.text):
        self.logger.info(tr.lang('window', 'message.text').format(message))

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
    def on_mouse_motion(self, x, y, dx, dy) -> None:
        pass

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
        pass

    @_call_screen_after
    def on_mouse_press(self, x, y, button, modifiers) -> None:
        self.logger.debug(
            tr.lang('window', 'mouse.press').format(
                [x, y], tr.lang('window', f'mouse.{mouse.buttons_string(button)}')
            )
        )

    @_call_screen_after
    def on_mouse_release(self, x, y, button, modifiers) -> None:
        self.logger.debug(
            tr.lang('window', 'mouse.release').format(
                [x, y], tr.lang('window', f'mouse.{mouse.buttons_string(button)}')
            )
        )

    @_call_screen_after
    def on_key_press(self, symbol, modifiers) -> None:
        if symbol == key.ESCAPE and not (modifiers & ~(key.MOD_NUMLOCK |
                                                       key.MOD_CAPSLOCK |
                                                       key.MOD_SCROLLLOCK)):
            self.dispatch_event('on_close')
        self.logger.debug(
            tr.lang('window', 'key.press').format(key.symbol_string(symbol), key.modifiers_string(modifiers)))

    @_call_screen_after
    def on_key_release(self, symbol, modifiers) -> None:
        self.logger.debug(
            tr.lang('window', 'key.release').format(key.symbol_string(symbol), key.modifiers_string(modifiers)))

    @_call_screen_after
    def on_file_drop(self, x, y, paths):
        ...

    @_call_screen_after
    def on_text(self, text):
        if text == '\r':
            self.logger.debug(tr.lang('window', 'text.new_line'))
        else:
            self.logger.debug(tr.lang('window', 'text.input').format(text))
            if text == 't':
                self.input_box.enabled = True

    @_call_screen_after
    def on_text_motion(self, motion):
        motion_string = key.motion_string(motion)
        self.logger.debug(tr.lang('window', 'text.motion').format(motion_string))

    @_call_screen_after
    def on_text_motion_select(self, motion):
        motion_string = key.motion_string(motion)
        self.logger.debug(tr.lang('window', 'text.motion_select').format(motion_string))

    @_call_screen_before
    def on_close(self, source: str = 'window') -> None:
        self.logger.info(tr.lang('window', 'game.stop_get').format(tr.lang('window', f'game.{source}_stop')))
        self.logger.info(tr.lang('window', 'game.stop'))
        self.fps_log.check_list = False
        DR_runtime.running = False
        if self.run_input:
            self.run_input = False
        self.save_info()
        super().on_close()
        self.logger.info(tr.lang('window', 'game.end'))
