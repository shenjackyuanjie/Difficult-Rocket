#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

# system function
import os
import sys
import time
import logging
import traceback
import configparser

from decimal import Decimal

if __name__ == '__main__':  # been start will not run this
    sys.path.append('/bin/libs')
    sys.path.append('/bin')

# Difficult_Rocket function
import translate

from Difficult_Rocket.api.Exp import *
from Difficult_Rocket.fps.fps_log import FpsLogger
from Difficult_Rocket.translate import tr
from Difficult_Rocket.command import line
from Difficult_Rocket.api import tools, new_thread

# libs function
local_lib = True
if local_lib:
    from libs import pyglet
    from libs.pyglet.window import key, mouse
else:
    import pyglet
    from pyglet.window import key, mouse


class Client:
    def __init__(self, net_mode='local'):
        start_time = time.time_ns()
        # logging
        self.logger = logging.getLogger('client')
        # config
        self.config = tools.load_file('configs/main.config')
        # value
        self.process_id = 'Client'
        self.process_name = 'Client process'
        self.process_pid = os.getpid()
        self.net_mode = net_mode
        self.caption = tools.name_handler(self.config['window']['caption'], {'version': self.config['runtime']['version']})
        self.window = ClientWindow(net_mode=self.net_mode,
                                   width=int(self.config['window']['width']),
                                   height=int(self.config['window']['height']),
                                   fullscreen=tools.format_bool(self.config['window']['full_screen']),
                                   caption=self.caption,
                                   resizable=tools.format_bool(self.config['window']['resizable']),
                                   visible=tools.format_bool(self.config['window']['visible']))
        self.logger.info(tr.lang('client', 'setup.done'))
        end_time = time.time_ns()
        self.use_time = end_time - start_time
        self.logger.info(tr.lang('client', 'setup.use_time').format(Decimal(self.use_time) / 1000000000))
        self.logger.debug(tr.lang('client', 'setup.use_time_ns').format(self.use_time))

    def start(self):
        self.window.start_game()  # 游戏启动
        # TODO 写一下服务端启动相关，还是需要服务端啊


class ClientWindow(pyglet.window.Window):

    def __init__(self, net_mode='local', *args, **kwargs):
        start_time = time.time_ns()
        super().__init__(*args, **kwargs)
        """
        :param dev_list: 共享内存
        :param dev_dic: 共享内存
        :param logger: logger
        :param net_mode: 网络模式 # local / ip
        """
        # logging
        self.logger = logging.getLogger('client')
        # value
        self.net_mode = net_mode
        self.run_input = False
        # configs
        pyglet.resource.path = ['textures']
        pyglet.resource.reindex()
        self.config_file = tools.load_file('configs/main.config')
        self.game_config = tools.load_file('configs/game.config')
        # dic
        self.environment = {}
        self.textures = {}  # all textures
        self.runtime = {}
        # FPS
        self.FPS = Decimal(int(self.config_file['runtime']['fps']))
        self.SPF = Decimal('1') / self.FPS
        self.fps_log = FpsLogger(stable_fps=int(self.FPS),
                                 wait_time=5)
        # batch
        self.part_batch = pyglet.graphics.Batch()
        self.label_batch = pyglet.graphics.Batch()
        # frame
        self.frame = pyglet.gui.Frame(self, order=20)
        self.M_frame = pyglet.gui.MovableFrame(self, modifier=key.LCTRL)
        # setup
        self.setup()
        # 命令显示
        self.command_group = pyglet.graphics.Group(0)
        self.command = line.CommandLine(x=50, y=30,  # 实例化
                                        width=self.width - 100, height=40,
                                        length=int(self.game_config['command']['show']),
                                        batch=self.label_batch, group=self.command_group)
        self.push_handlers(self.command)
        self.command.set_handler('on_command', self.on_command)
        self.command.set_handler('on_message', self.on_message)
        # fps显示
        self.fps_label = pyglet.text.Label(x=10, y=self.height - 10,
                                           width=self.width - 20, height=20,
                                           anchor_x='left', anchor_y='top',
                                           font_name=translate.鸿蒙简体, font_size=20,
                                           multiline=True,
                                           batch=self.label_batch, group=self.command_group)
        # 设置刷新率
        pyglet.clock.schedule_interval(self.update, float(self.SPF))
        # 完成设置后的信息输出
        self.logger.info(tr.lang('window', 'setup.done'))
        self.logger.info(tr.lang('window', 'os.pid_is').format(os.getpid(), os.getppid()))
        end_time = time.time_ns()
        self.use_time = end_time - start_time
        self.logger.info(tr.lang('window', 'setup.use_time').format(Decimal(self.use_time) / 1000000000))
        self.logger.debug(tr.lang('window', 'setup.use_time_ns').format(self.use_time))

    def setup(self):
        self.load_fonts().join()

    @new_thread('window load_fonts')
    def load_fonts(self):
        file_path = './libs/fonts/HarmonyOS_Sans/'
        ttf_files = os.listdir(file_path)
        self.logger.info(tr.lang('window', 'fonts.found').format(ttf_files))
        for ttf_folder in ttf_files:
            for ttf_file in os.listdir(f'{file_path}{ttf_folder}'):
                if not ttf_file[-4:] == '.ttf':
                    continue
                pyglet.font.add_file(f'{file_path}{ttf_folder}/{ttf_file}')

    # @new_thread('window load_editor')
    def load_Editor(self):
        pass

    def start_game(self) -> None:
        self.run_input = True
        self.read_input()
        pyglet.app.run()

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
        config_file = configparser.ConfigParser()
        config_file.read('configs/main.config')
        config_file['window']['width'] = str(self.width)
        config_file['window']['height'] = str(self.height)
        config_file.write(open('configs/main.config', 'w', encoding='utf-8'))

    """
    draws and some event
    """

    def update(self, tick: float):
        decimal_tick = Decimal(str(tick)[:10])
        self.FPS_update(decimal_tick)
        self.fps_log.update_tick(Decimal(tick))

    def FPS_update(self, tick: Decimal):
        now_FPS = pyglet.clock.get_fps()
        self.fps_log.update_tick(tick)
        self.fps_label.text = f'FPS: {now_FPS:_>10.1f} \n{1/tick} \n{self.fps_log.max_fps:_>10.1f} {self.fps_log.min_fps:>5.1f}'

    def on_draw(self, *dt):
        self.clear()
        self.draw_batch()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.fps_label.y = height - 10

    def draw_batch(self):
        self.part_batch.draw()
        self.label_batch.draw()

    """
    command line event
    """

    def on_command(self, command: line.CommandText):
        self.logger.info(tr.lang('window', 'command.text').format(command))
        if command.match('stop'):
            self.dispatch_event('on_close', 'command')  # source = command
        elif command.match('fps'):
            if command.match('log'):
                self.logger.debug(self.fps_log.fps_list)
            elif command.match('max'):
                self.logger.info(self.fps_log.max_fps)
                self.command.push_line(self.fps_log.max_fps, block_line=True)
            elif command.match('min'):
                self.logger.info(self.fps_log.min_fps)
                self.command.push_line(self.fps_log.min_fps, block_line=True)
        elif command.match('default'):
            self.set_size(int(self.config_file['window_default']['width']), int(self.config_file['window_default']['height']))

    def on_message(self, message: line.CommandLine.text):
        self.logger.info(tr.lang('window', 'message.text').format(message))

    """
    keyboard and mouse input
    """

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers) -> None:
        pass

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        self.logger.debug(tr.lang('window', 'mouse.press').format([x, y], tr.lang('window', 'mouse.{}'.format(mouse.buttons_string(button)))))

    def on_mouse_release(self, x, y, button, modifiers) -> None:
        self.logger.debug(tr.lang('window', 'mouse.release').format([x, y], tr.lang('window', 'mouse.{}'.format(mouse.buttons_string(button)))))

    def on_key_press(self, symbol, modifiers) -> None:
        if symbol == key.ESCAPE and not (modifiers & ~(key.MOD_NUMLOCK |
                                                       key.MOD_CAPSLOCK |
                                                       key.MOD_SCROLLLOCK)):
            self.dispatch_event('on_close')
        self.logger.debug(tr.lang('window', 'key.press').format(key.symbol_string(symbol), key.modifiers_string(modifiers)))

    def on_key_release(self, symbol, modifiers) -> None:
        self.logger.debug(tr.lang('window', 'key.release').format(key.symbol_string(symbol), key.modifiers_string(modifiers)))

    def on_text(self, text):
        if text == '\r':
            self.logger.debug(tr.lang('window', 'text.new_line'))
        else:
            self.logger.debug(tr.lang('window', 'text.input').format(text))

    def on_text_motion(self, motion):
        motion_string = key.motion_string(motion)
        self.logger.debug(tr.lang('window', 'text.motion').format(motion_string))

    def on_text_motion_select(self, motion):
        motion_string = key.motion_string(motion)
        self.logger.debug(tr.lang('window', 'text.motion_select').format(motion_string))

    def on_close(self, source: str = 'window') -> None:
        self.logger.info(tr.lang('window', 'game.stop_get').format(tr.lang('window', f'game.{source}_stop')))
        self.logger.info(tr.lang('window', 'game.stop'))
        self.fps_log.check_list = False
        if self.run_input:
            self.run_input = False
        self.save_info()
        super().on_close()
        self.logger.info(tr.lang('window', 'game.end'))
