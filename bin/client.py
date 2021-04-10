"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import os
import sys

sys.path.append('./bin/libs/')
sys.path.append('./')
import time
import pyglet
from pyglet.window import key
from pyglet.window import mouse
import multiprocessing as mp

try:
    from bin import tools
    from bin import configs
except (ModuleNotFoundError, ImportError, ImportWarning):
    import tools
    import configs


class client(mp.Process):
    def __init__(self, logger, dev_dic=None, dev_list=None, language='zh-cn', net_mode='local'):
        mp.Process.__init__(self)
        # logging
        self.logger = logger
        # share memory
        self.dev_list = dev_list
        self.dev_dic = dev_dic
        # lang
        self.lang = tools.config('configs/sys_value/lang/%s.json5' % language, 'client')
        # value
        self.process_id = 'Client'
        self.process_name = 'Client process'
        self.process_pid = os.getpid()
        self.view = 'space'
        self.net_mode = net_mode
        self.window_config = tools.config('configs/sys_value/window.json5')
        self.caption = self.window_config['caption']
        self.caption = configs.name_handler(self.caption, {'version': self.window_config['caption_option']['version']})
        self.window = window(logger=logger,
                             dev_dic=dev_dic,
                             dev_list=dev_list,
                             language=language,
                             net_mode=net_mode,
                             width=int(self.window_config['width']),
                             height=int(self.window_config['height']),
                             fullscreen=tools.c_b(self.window_config['full_screen']),
                             caption=self.caption,
                             resizable=tools.c_b(self.window_config['resizable']),
                             visible=tools.c_b(self.window_config['visible']))
        self.log_config()

    def log_config(self):
        self.logger.info('%s: %s %s' % (self.lang['os.pid_is1'], self.process_pid, self.lang['os.pid_is2']))

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
        self.FPS = int(tools.config('configs/sys_value/window.json5')['fps'])
        self.SPF = 1.0 / self.FPS
        self.view = 'space'
        self.net_mode = net_mode
        # FPS
        self.max_fps = [self.FPS, time.time()]
        self.min_fps = [self.FPS, time.time()]
        self.fps_wait = 5
        # lang
        self.lang = tools.config('configs/sys_value/lang/%s.json5' % language, 'client')
        # configs
        self.view = tools.config('configs/view.json5')
        self.map_view = [configs.basic_poi(poi_type='chunk')]
        self.part_list = tools.config('configs/sys_value/parts.json5')
        pyglet.resource.path = ['textures']
        pyglet.resource.reindex()
        # dic
        self.button_hitbox = {}
        self.button_toggled = {}
        self.ships = {}  # all ship(part)
        self.planet_system = tools.config('configs/sys_value/planet.json5')  # hole planet system
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
        # values
        # net_mode
        if self.net_mode == 'local':
            pass

        # parts textures
        self.textures['part'] = {}
        parts = tools.config('configs/sys_value/parts.json5')
        for part in parts:
            path = parts[part][2][0]
            part_image = pyglet.resource.image(path)
            self.textures['part'][part] = part_image

        # runtimes textures
        self.textures['runtime'] = {}
        runtimes = tools.config('configs/sys_value/runtime.json5')
        # load textures
        for runtime in runtimes['textures']:
            path = runtimes['textures'][runtime]
            runtime_image = pyglet.resource.image(path)
            self.textures['runtime'][runtime] = runtime_image
        # load button's textures
        for runtime in runtimes['button']:
            if runtime == 'logic':
                continue
            path = runtimes['button'][runtime]
            runtime_image = pyglet.resource.image(path)
            runtime_sprite = pyglet.sprite.Sprite(img=runtime_image, batch=self.runtime_batch, x=self.width + 1,
                                                  y=self.height + 1)
            # self.textures['runtime'][runtime] = runtime_image
            self.textures['runtime'][runtime] = runtime_sprite
            self.button_hitbox[runtime] = [runtime_image.width, runtime_image.height]
            self.button_toggled[runtime] = -1

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
        for hit_box in self.button_hitbox:
            box_ = self.button_hitbox[hit_box]
            button = self.textures['runtime'][hit_box]
            box = [button.x, button.y, button.x + button.width, button.y + button.height]
            self.button_hitbox[hit_box] = box

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
        self.textures['runtime']['trash_can'].blit(x=self.width - 90, y=self.height - 90)
        # button tool bar
        # start from 20 20
        # between 30
        # size 50*50
        tool_y = 25
        back = 0
        while back < self.width:
            self.textures['runtime']['toolbar_light'].blit(x=back, y=0)
            back += self.textures['runtime']['toolbar_light'].width - 1
        self.textures['runtime']['to_menu'].x = 20
        self.textures['runtime']['to_menu'].y = tool_y
        self.textures['runtime']['add_part'].x = 100
        self.textures['runtime']['add_part'].y = tool_y
        self.textures['runtime']['stage'].x = 180
        self.textures['runtime']['stage'].y = tool_y
        self.textures['runtime']['zoom'].x = 260
        self.textures['runtime']['zoom'].y = tool_y
        self.textures['runtime']['play'].x = self.width - 50 - 20
        self.textures['runtime']['play'].y = tool_y
        if self.button_toggled['zoom'] != -1:
            self.textures['runtime']['zoom_in'].x = 260 - 40
            self.textures['runtime']['zoom_in'].y = tool_y + 25 + 50
            self.textures['runtime']['zoom_out'].x = 260 + 40
            self.textures['runtime']['zoom_out'].y = tool_y + 25 + 50
        else:
            self.button_toggled['zoom_in'] = -1
            self.button_toggled['zoom_out'] = -1
            self.textures['runtime']['zoom_in'].x = self.width + 1
            self.textures['runtime']['zoom_out'].x = self.width + 1

        # //todo 把所有要素都加进来+整个设置图标+布局

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
        self.logger.debug('按键移动 %s %s %s %s' % (x, y, dx, dy))

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.logger.debug('按键拖拽 %s %s %s %s %s %s' %(x, y, dx, dy, buttons, modifiers))

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.logger.debug('左键！ 在 x:%s y:%s' % (x, y))
            for hit_box in self.button_hitbox:
                box = self.button_hitbox[hit_box]
                if (box[0] <= x <= box[2]) and (box[1] <= y <= box[3]):
                    self.button_toggled[hit_box] *= -1
                    self.logger.debug('%s %s %s' % (hit_box,
                                                    self.lang['button.been_press'],
                                                    self.button_toggled[hit_box]))
                    break
        elif button == mouse.RIGHT:
            self.logger.debug('右键！ 在 x:%s y:%s' % (x, y))

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE and not (modifiers & ~(key.MOD_NUMLOCK |
                                                       key.MOD_CAPSLOCK |
                                                       key.MOD_SCROLLLOCK)):
            self.dispatch_event('on_close')

    def on_key_release(self, symbol, modifiers):
        pass
