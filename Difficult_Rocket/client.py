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
import random
import logging
import threading
import configparser
import multiprocessing

from multiprocessing import Pipe
from multiprocessing.connection import Connection

if __name__ == '__main__':  # been start will not run this
    sys.path.append('/bin/libs')
    sys.path.append('/bin')

# Difficult_Rocket function
from Difficult_Rocket import crash
from Difficult_Rocket.api.Exp import *
from Difficult_Rocket.api.translate import tr
from Difficult_Rocket.drag_sprite import DragSprite
from Difficult_Rocket.api import tools, config, new_thread, thread

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
        # logging
        self.logger = logging.getLogger('client')
        # config
        self.config = tools.config('configs/main.config')
        # lang
        self.lang = tools.config('configs/lang/%s.json5' % self.config['runtime']['language'], 'client')
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

    def start(self):
        self.window.start_game()  # 游戏启动
        # TODO 写一下服务端启动相关，还是需要服务端啊


class ClientWindow(pyglet.window.Window):

    def __init__(self, net_mode='local', *args, **kwargs):
        self.times = [time.time()]
        super().__init__(*args, **kwargs)
        """
        :param dev_list: 共享内存
        :param dev_dic: 共享内存
        :param logger: logger
        :param net_mode: 网络模式 # local / ip
        """
        # logging
        self.logger = logging.getLogger('client')
        # share memory
        # self.dev_list = dev_list
        # self.dev_dic = dev_dic
        # value
        self.net_mode = net_mode
        self.run_input = False
        # configs
        pyglet.resource.path = ['textures']
        pyglet.resource.reindex()
        self.config_file = tools.config('configs/main.config')
        self.FPS = int(self.config_file['runtime']['fps'])
        self.SPF = 1.0 / self.FPS
        # lang
        self.lang = tools.config('configs/lang/%s.json5' % self.config_file['runtime']['language'], 'client')
        # dic
        self.environment = {}
        self.textures = {}  # all textures
        self.runtime = {}
        # list
        # FPS
        self.max_fps = [self.FPS, time.time()]
        self.min_fps = [self.FPS, time.time()]
        self.fps_wait = 5
        # batch
        self.part_batch = pyglet.graphics.Batch()
        self.label_batch = pyglet.graphics.Batch()
        # frame
        self.frame = pyglet.gui.Frame(self)
        # setup
        self.setup()
        self.info_label = pyglet.text.Label(x=10, y=self.height - 10,
                                            anchor_x='left', anchor_y='top',
                                            batch=self.label_batch)
        pyglet.clock.schedule_interval(self.update, self.SPF)
        self.times.append(time.time())
        self.times.append(self.times[1] - self.times[0])
        self.logger.debug(self.times[2])
        self.logger.info(self.lang['setup.done'])

    @new_thread('client_load_environment')
    def load_environment(self) -> None:
        # load parts info
        self.environment['parts'] = config('configs/sys_value/parts.json5')
        try:
            self.load_textures()
        except TexturesError:
            raise

    @new_thread('client_load_textures')
    def load_textures(self) -> None:
        # load parts
        self.textures['parts'] = {}
        for part in self.environment['parts']:
            pass

    def setup(self):
        self.logger.info(self.lang['os.pid_is'].format(os.getpid(), os.getppid()))
        image = pyglet.image.load('textures/Editor/PartButton.png')
        self.textures['test'] = DragSprite(10, 20, image, batch=self.label_batch, drag_by_all=False, drag_out_window=True)
        self.load_environment()

    def start_game(self) -> None:
        self.run_input = True
        # self.input_line = threading.Thread(target=self.read_input, name='client_read_line', daemon=True)
        # self.input_line.start()
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
        self.FPS_update(tick)

    def FPS_update(self, tick: float):
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
        self.info_label.text = 'FPS: {:.1f} {:.1f} ({:.1f}/{:.1f}) | MSPF: {:.5f} '.format(now_FPS, 1 / tick, self.max_fps[0], self.min_fps[0], tick)

    def on_draw(self):
        self.clear()
        self.draw_batch()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.info_label.y = height - 10

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
        self.textures['test'].on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        pass

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button == mouse.LEFT:
            self.logger.debug(self.lang['mouse.press'].format([x, y], self.lang['mouse.left']))
        elif button == mouse.RIGHT:
            self.logger.debug(self.lang['mouse.press'].format([x, y], self.lang['mouse.right']))
        self.textures['test']._sprite.rotation = random.randint(0, 360)
        self.textures['test'].on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers) -> None:
        self.logger.debug(self.lang['mouse.release'].format([x, y], self.lang['mouse.right']))
        self.textures['test'].on_mouse_release(x, y, button, modifiers)

    def on_key_press(self, symbol, modifiers) -> None:
        if symbol == key.ESCAPE and not (modifiers & ~(key.MOD_NUMLOCK |
                                                       key.MOD_CAPSLOCK |
                                                       key.MOD_SCROLLLOCK)):
            self.dispatch_event('on_close')

    def on_key_release(self, symbol, modifiers) -> None:
        pass

    def on_close(self) -> None:
        self.run_input = False
        # self.input_line.join()
        config_file = configparser.ConfigParser()
        config_file.read('configs/main.config')
        config_file['window']['width'] = str(self.width)
        config_file['window']['height'] = str(self.height)
        config_file.write(open('configs/main.config', 'w', encoding='utf-8'))
        super(ClientWindow, self).on_close()
