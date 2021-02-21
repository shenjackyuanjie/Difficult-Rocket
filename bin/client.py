"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import os
import time
import pyglet
import random
from pyglet import image
import multiprocessing as mp

try:
    # been import use
    from bin import configs
    from bin import tools
except (ModuleNotFoundError, ImportError, ImportWarning):
    # editing use
    import configs
    import tools


class client(mp.Process):
    def __init__(self, logger, dev_dic=None, dev_list=None, language='zh-cn', net_mode='local'):
        mp.Process.__init__(self)
        # logging
        self.logger = logger
        # share memory
        self.dev_list = dev_list
        self.dev_dic = dev_dic
        # value
        self.process_id = 'Client'
        self.process_name = 'Client process'
        self.process_pid = os.getpid()
        self.view = 'space'
        self.net_mode = net_mode
        self.window_config = tools.config('sys_value/window.json5')
        self.window = window(logger=logger,
                             dev_dic=dev_dic,
                             dev_list=dev_list,
                             language=language,
                             net_mode=net_mode,
                             width=int(self.window_config['width']),
                             height=int(self.window_config['height']),
                             fullscreen=tools.c_b(self.window_config['full_screen']),
                             caption=str(self.window_config['caption']),
                             visible=tools.c_b(self.window_config['visible']))
        self.log_config()

    def log_config(self):
        self.logger.info('client is running on pid : %s' % self.process_pid)

    def run(self) -> None:
        pyglet.app.run()


class window(pyglet.window.Window):

    def __init__(self, logger, dev_dic=None, dev_list=None, language='zh-cn', net_mode='local', *args, **kwargs):
        super(window, self).__init__(*args, **kwargs)
        """
        :param dev_list: 共享内存
        :param dev_dic: 共享内存
        :param logger: logger
        :param net_mode: 网络模式 # local / ip
        """
        # logging
        self.logger = logger
        # share memory
        self.dev_list = dev_list
        self.dev_dic = dev_dic
        # value
        self.FPS = 60
        self.SPF = 1.0 / self.FPS
        self.view = 'space'
        self.net_mode = net_mode
        # configs
        self.lang = tools.config('sys_value/lang/%s.json5' % language)
        self.view = tools.config('configs/view.json5')
        self.map_view = [configs.basic_poi(poi_type='chunk')]
        self.part_list = tools.config('sys_value/parts.json5')
        # dic
        self.ships = {}  # all ship(part)
        self.planet_system = tools.config('sys_value/planet.json5')  # hole planet system
        # list
        # batch
        self.part_batch = pyglet.graphics.Batch()
        self.label_batch = pyglet.graphics.Batch()
        self.runtime_batch = pyglet.graphics.Batch()
        # window
        self.logger.info('client setup done!')
        self.textures = {}
        # setup
        self.setup()
        pyglet.clock.schedule_interval(self.update(), self.SPF)

    def setup(self):
        # net_mode
        if self.net_mode == 'local':
            pass
        # parts
        self.textures['part'] = {}
        parts = tools.config('sys_value/parts.json5')
        for part in parts:
            path = parts[part][2][0]
            part_image = image.load('textures/' + path)
            self.textures['part'][part] = part_image

        # tests
        self.info_label = pyglet.text.Label(text='test %s' % pyglet.clock.get_fps(),
                                            x=10, y=self.height - 10,
                                            anchor_x='left', anchor_y='top',
                                            batch=self.label_batch)

    # draws

    def update(self):
        self.info_label.x = random.randint(100, 500)
        self.info_label.y = random.randint(100, 500)

    def on_draw(self):
        self.draw_batch()
        print(time.time())

    def draw_batch(self):
        self.clear()
        self.part_batch.draw()
        self.runtime_batch.draw()
        self.label_batch.draw()

    def build_draw(self):
        pass

    def space_draw(self):
        # render parts
        for ship in self.ships:
            # get ship poi
            ship_poi = ship['brain'][3]
            distances = tools.distance(ship_poi, self.map_view)
            for part in ship:
                pass

    def draw_label(self):
        pass

    """
    keyboard and mouse input
    """

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass
