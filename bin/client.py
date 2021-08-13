"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""
import configparser
import logging
import multiprocessing as mp
import os
import sys
import time

sys.path.append('./bin/libs/')
sys.path.append('./')
import pyglet
from pyglet.window import key
from pyglet.window import mouse

try:
    from bin import tools
    from bin import configs
except (ModuleNotFoundError, ImportError, ImportWarning):
    import tools
    import configs


class Client:
    def __init__(self, dev_dic=None, dev_list=None, net_mode='local'):
        pass
        # mp.Process.__init__(self)
        # logging
        self.logger = logging.getLogger('client')
        # share memory
        self.dev_list = dev_list
        self.dev_dic = dev_dic
        # config
        self.config = tools.config('configs/main.config')
        # lang
        self.lang = tools.config('configs/lang/%s.json5' % self.config['runtime']['language'], 'client')
        # value
        self.process_id = 'Client'
        self.process_name = 'Client process'
        self.process_pid = os.getpid()
        self.view = 'space'
        self.net_mode = net_mode
        self.caption = tools.name_handler(self.config['window']['caption'], {'version': self.config['runtime']['version']})
        self.window = ClientWindow(dev_dic=self.dev_dic,
                                   dev_list=self.dev_list,
                                   net_mode=self.net_mode,
                                   width=int(self.config['window']['width']),
                                   height=int(self.config['window']['height']),
                                   fullscreen=tools.format_bool(self.config['window']['full_screen']),
                                   caption=self.caption,
                                   resizable=tools.format_bool(self.config['window']['resizable']),
                                   visible=tools.format_bool(self.config['window']['visible']))

    def run(self) -> None:
        pyglet.app.run()


class ClientWindow(pyglet.window.Window):

    def __init__(self, dev_dic=None, dev_list=None, net_mode='local', *args, **kwargs):
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
        self.dev_list = dev_list
        self.dev_dic = dev_dic
        # value
        self.view = 'space'
        self.net_mode = net_mode
        self.config_file = tools.config('configs/main.config')
        self.FPS = int(self.config_file['runtime']['fps'])
        self.SPF = 1.0 / self.FPS
        # FPS
        self.max_fps = [self.FPS, time.time()]
        self.min_fps = [self.FPS, time.time()]
        self.fps_wait = 5
        # lang
        self.lang = tools.config('configs/lang/%s.json5' % self.config_file['runtime']['language'], 'client')
        # configs
        pyglet.resource.path = ['textures']
        pyglet.resource.reindex()
        # dic
        self.button_hitbox = {}
        self.button_toggled = {}
        # list
        # batch
        self.part_batch = pyglet.graphics.Batch()
        self.label_batch = pyglet.graphics.Batch()
        self.runtime_batch = pyglet.graphics.Batch()
        # window
        self.logger.info(self.lang['setup.done'])
        self.textures = {}
        # setup
        self.setup()
        pyglet.clock.schedule_interval(self.update, self.SPF)

    def setup(self):
        self.logger.info(self.lang['os.pid_is'].format(os.getpid(), os.getppid()))
        # values
        # net_mode
        if self.net_mode == 'local':
            pass

        # info_label
        self.info_label = pyglet.text.Label(text='test %s' % pyglet.clock.get_fps(),
                                            x=10, y=self.height - 10,
                                            anchor_x='left', anchor_y='top',
                                            batch=self.label_batch)

    # draws

    def update(self, ree):
        self.FPS_update()
        self.hit_box_update()

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
        self.info_label.anchor_x = 'left'
        self.info_label.anchor_y = 'top'
        self.info_label.x = 10
        self.info_label.y = self.height - 10

    def hit_box_update(self):
        pass

    def on_draw(self):
        self.clear()
        self.build_draw()
        self.draw_batch()

    def draw_batch(self):
        self.part_batch.draw()
        self.runtime_batch.draw()
        self.label_batch.draw()

    def build_draw(self):
        pass
        # //todo 重写整个渲染机制

    def draw_label(self):
        pass

    """
    keyboard and mouse input
    """

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        # self.logger.debug('按键移动 %s %s %s %s' % (x, y, dx, dy))
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers) -> None:
        # self.logger.debug('按键拖拽 %s %s %s %s %s %s' %(x, y, dx, dy, buttons, modifiers))
        pass

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button == mouse.LEFT:
            self.logger.debug(self.lang['mouse.press_at'].format([x, y], self.lang['mouse.left']))
        elif button == mouse.RIGHT:
            self.logger.debug(self.lang['mouse.press_at'].format([x, y], self.lang['mouse.right']))

    def on_mouse_release(self, x, y, button, modifiers) -> None:
        pass

    def on_key_press(self, symbol, modifiers) -> None:
        if symbol == key.ESCAPE and not (modifiers & ~(key.MOD_NUMLOCK |
                                                       key.MOD_CAPSLOCK |
                                                       key.MOD_SCROLLLOCK)):
            self.dispatch_event('on_close')

    def on_key_release(self, symbol, modifiers) -> None:
        pass

    def on_close(self) -> None:
        config_file = configparser.ConfigParser()
        config_file.read('configs/main.config')
        config_file['window']['width'] = str(self.width)
        config_file['window']['height'] = str(self.height)
        config_file.write(open('configs/main.config', 'w', encoding='utf-8'))
        # pyglet source code
        self.has_exit = True
        from pyglet import app
        if app.event_loop.is_running:
            self.close()
