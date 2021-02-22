"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import os
import time
import pyglet
import random
from pyglet.window import key
from pyglet.window import mouse
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
        # lang
        self.lang = tools.config('sys_value/lang/%s.json5' % language, 'client')
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
        self.logger.info('%s: %s%s' % (self.lang['os.pid_is1'], self.process_pid, self.lang['os.pid_is2']))

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
        # FPS
        self.max_fps = [self.FPS, time.time()]
        self.min_fps = [self.FPS, time.time()]
        self.fps_wait = 5
        # lang
        self.lang = tools.config('sys_value/lang/%s.json5' % language, 'client')
        # configs
        self.view = tools.config('configs/view.json5')
        self.map_view = [configs.basic_poi(poi_type='chunk')]
        self.part_list = tools.config('sys_value/parts.json5')
        pyglet.resource.path = ['textures']
        pyglet.resource.reindex()
        # dic
        self.ships = {}  # all ship(part)
        self.planet_system = tools.config('sys_value/planet.json5')  # hole planet system
        # list
        # batch
        self.part_batch = pyglet.graphics.Batch()
        self.label_batch = pyglet.graphics.Batch()
        self.runtime_batch = pyglet.graphics.Batch()
        # window
        self.logger.info('%s' % self.lang['setup.done'])
        self.textures = {}
        # setup
        self.setup()
        pyglet.clock.schedule_interval(self.update, self.SPF)

    def setup(self):
        # net_mode
        if self.net_mode == 'local':
            pass
        # parts textures
        self.textures['part'] = {}
        parts = tools.config('sys_value/parts.json5')
        for part in parts:
            path = parts[part][2][0]
            part_image = pyglet.resource.image(path)
            self.textures['part'][part] = part_image
        # runtimes textures
        self.textures['runtime'] = {}
        runtimes = tools.config('sys_value/runtime.json5')
        for runtime in runtimes:
            path = runtimes[runtime]
            runtime_image = pyglet.resource.image(path)
            self.textures['runtime'][runtime] = runtime_image

        # tests
        self.info_label = pyglet.text.Label(text='test %s' % pyglet.clock.get_fps(),
                                            x=10, y=self.height - 10,
                                            anchor_x='left', anchor_y='top',
                                            batch=self.label_batch)

    # draws

    def update(self, ree):
        self.FPS_update()

    def FPS_update(self):
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
        self.info_label.text = 'now FPS: %03d max FPS: %02d  min FPS: %02d' % (
            now_FPS, self.max_fps[0], self.min_fps[0])

    def on_draw(self):
        self.clear()
        self.build_draw()
        self.draw_batch()

    def draw_batch(self):
        self.part_batch.draw()
        self.runtime_batch.draw()
        self.label_batch.draw()

    def build_draw(self):
        self.textures['runtime']['trash_can'].blit(x=self.width - 90, y=self.height - 90)
        self.textures['runtime']['add_part'].blit(x=10, y=10)

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
        print(x, y, button, modifiers)
        if button == mouse.LEFT:
            self.logger.info('左键！')
        elif button == mouse.RIGHT:
            self.logger.info('右键！')

    def on_key_press(self, symbol, modifiers):
        print(symbol, modifiers)
        if symbol == key.ESCAPE and not (modifiers & ~(key.MOD_NUMLOCK |
                                                       key.MOD_CAPSLOCK |
                                                       key.MOD_SCROLLLOCK)):
            self.dispatch_event('on_close')

    def on_key_release(self, symbol, modifiers):
        pass
