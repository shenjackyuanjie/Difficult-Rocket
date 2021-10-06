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
import configparser

from decimal import Decimal

if __name__ == '__main__':  # been start will not run this
    sys.path.append('/bin/libs')
    sys.path.append('/bin')

# Difficult_Rocket function
from Difficult_Rocket import guis
from Difficult_Rocket.api import command
from Difficult_Rocket.api.translate import tr
from Difficult_Rocket.api import tools, new_thread, translate

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
        self.FPS = Decimal(int(self.config_file['runtime']['fps']))
        self.SPF = Decimal('1') / self.FPS
        # dic
        self.environment = {}
        self.textures = {}  # all textures
        self.runtime = {}
        # FPS
        self.max_fps = [self.FPS, time.time()]
        self.min_fps = [self.FPS, time.time()]
        self.fps_wait = 5
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
        self.command = command.CommandLine(x=50, y=30,
                                           width=self.width-100, height=40,
                                           length=int(self.game_config['command']['show']),
                                           batch=self.label_batch, group=self.command_group)
        self.push_handlers(self.command)
        # fps显示
        self.fps_label = pyglet.text.Label(x=10, y=self.height - 10,
                                           anchor_x='left', anchor_y='top',
                                           font_name=translate.鸿蒙简体, font_size=20,
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
        self.load_fonts()
        # print(pyglet.font.have_font('HarmonyOS_Sans_Black'))

    # @new_thread('client load_fonts')
    def load_fonts(self):
        file_path = './libs/fonts/HarmonyOS Sans/'
        ttf_files = os.listdir(file_path)
        self.logger.info(tr.lang('window', 'fonts.found').format(ttf_files))
        for ttf_file in ttf_files:
            pyglet.font.add_directory(f'{file_path}{ttf_file}')

    @new_thread('client load_editor')
    def load_Editor(self):
        pass

    def start_game(self) -> None:
        self.run_input = True
        # self.read_thread = threading.Thread(target=self.read_input, name='client_read_input')
        # self.read_thread.start()
        # crash.all_thread.append(self.read_thread)
        pyglet.app.run()

    def read_input(self):
        self.logger.debug('read_input start')
        while self.run_input:
            get = input('<<<')
            self.logger.info(get)
            if get == 'stop':
                self.run_input = False
        self.logger.debug('read_input end')

    """
    draws and some event
    """

    def update(self, tick: float):
        decimal_tick = Decimal(tick)
        self.FPS_update(decimal_tick)

    def FPS_update(self, tick: Decimal):
        now_FPS = pyglet.clock.get_fps()
        if now_FPS > self.max_fps[0]:
            self.max_fps = [now_FPS, time.time()]
        elif now_FPS < self.min_fps[0]:
            self.min_fps = [now_FPS, time.time()]
        else:
            if (time.time() - self.max_fps[1]) > self.fps_wait:
                self.max_fps = [self.FPS, time.time()]
            elif (time.time() - self.min_fps[1]) > self.fps_wait:
                self.min_fps = [self.FPS, time.time()]
        self.fps_label.text = 'FPS: {:.1f} {:.1f} ({:.1f}/{:.1f}) | MSPF: {:.5f} '.format(now_FPS, 1 / tick, self.max_fps[0], self.min_fps[0], tick)

    def on_draw(self):
        self.clear()
        self.draw_batch()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.fps_label.y = height - 10

    def draw_batch(self):
        self.part_batch.draw()
        self.label_batch.draw()


    """
    keyboard and mouse input
    """

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        # self.logger.debug('按键移动 %s %s %s %s' % (x, y, dx, dy))
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers) -> None:
        # self.logger.debug('按键拖拽 %s %s %s %s %s %s' % (x, y, dx, dy, buttons, modifiers))
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

    def on_close(self) -> None:
        self.run_input = False
        # self.input_line.join()
        config_file = configparser.ConfigParser()
        config_file.read('configs/main.config')
        config_file['window']['width'] = str(self.width)
        config_file['window']['height'] = str(self.height)
        config_file.write(open('configs/main.config', 'w', encoding='utf-8'))
        super().on_close()
