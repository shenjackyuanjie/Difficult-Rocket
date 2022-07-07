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
from fractions import Fraction

if __name__ == '__main__':  # been start will not run this
    sys.path.append('/bin/libs')
    sys.path.append('/bin')

# SR tool function
from SRtool import translate
from SRtool.api.Exp import *
from SRtool.translate import tr
from SRtool.command import line
from SRtool.api import tools, new_thread

# libs function
from libs import pyglet
from libs import xmltodict
from libs.pyglet import shapes
from libs.pyglet.graphics import Batch
from libs.pyglet.window import key, mouse


class Client:
    def __init__(self):
        start_time = time.time_ns()
        # logging
        self.logger = logging.getLogger('client')
        # config
        self.config = tools.load_file('configs/main.config')
        # value
        self.process_id = 'Client'
        self.process_name = 'Client process'
        self.process_pid = os.getpid()
        self.caption = tools.name_handler(self.config['window']['caption'], {'version': self.config['runtime']['version']})
        self.window = ClientWindow(width=int(self.config['window']['width']),
                                   height=int(self.config['window']['height']),
                                   fullscreen=tools.format_bool(self.config['window']['full_screen']),
                                   caption=self.caption,
                                   resizable=tools.format_bool(self.config['window']['resizable']),
                                   visible=tools.format_bool(self.config['window']['visible']),
                                   file_drops=True)
        self.logger.info(tr.lang('client', 'setup.done'))
        end_time = time.time_ns()
        self.use_time = end_time - start_time
        self.logger.info(tr.lang('client', 'setup.use_time').format(Decimal(self.use_time) / 1000000000))
        self.logger.debug(tr.lang('client', 'setup.use_time_ns').format(self.use_time))

    def start(self):
        self.window.start_game()  # 游戏启动
        # TODO 写一下服务端启动相关，还是需要服务端啊


class ClientWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
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
        self.run_input = False
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        # configs
        pyglet.resource.path = ['./textures/', './files']
        pyglet.resource.reindex()
        self.config_file = tools.load_file('configs/main.config')
        self.game_config = tools.load_file('configs/game.config')
        # dic
        self.environment = {}
        self.textures = {}  # all textures
        self.runtime = {}
        self.坐标轴 = {'batch': Batch()}
        self.part_list = {}
        self.坐标点 = {'x': {}, 'y': {}}
        # FPS
        self.FPS = Decimal(int(self.config_file['runtime']['fps']))
        self.SPF = Decimal('1') / self.FPS
        # batch
        self.part_batch = Batch()
        self.label_batch = Batch()
        # frame
        self.frame = pyglet.gui.Frame(self, order=20)
        self.M_frame = pyglet.gui.MovableFrame(self, modifier=key.LCTRL)
        self.back_ground = shapes.Rectangle(0, 0, self.width, self.height, color=(60, 63, 65))
        icon = pyglet.resource.image('icon.png')
        self.set_icon(icon)
        del icon
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
        self.load_fonts().join()
        self.加载坐标轴()

    def 加载坐标轴(self):
        self.坐标轴['x'] = shapes.Line(x=0, y=self.center_y,
                                    x2=self.width, y2=self.center_y,
                                    width=3,
                                    batch=self.坐标轴['batch'])
        self.坐标轴['y'] = shapes.Line(x=self.center_x, y=0,
                                    x2=self.center_x, y2=self.height,
                                    width=3,
                                    batch=self.坐标轴['batch'])
        self.坐标轴['x'].color = (204, 102, 110)
        self.坐标轴['x'].opacity = 250
        self.坐标轴['y'].color = (204, 102, 110)
        self.坐标轴['y'].opacity = 250
        self.坐标轴['scale'] = 60
        self.坐标轴['long'] = 5
        self.坐标轴['point_opacity'] = 250
        self.加载坐标点(True)

    # @new_thread('坐标点加载')

    def 加载坐标轴上的点(self, name: str):
        del self.坐标点[name]
        self.坐标点[name] = {}
        for i in range(-self.坐标轴[f'scale_{name}'], self.坐标轴[f'scale_{name}'] + 1):
            if name == 'x':
                x, y, x2, y2 = self.center_x + (i * self.坐标轴['scale']), self.center_y - self.坐标轴['long'], \
                               self.center_x + (i * self.坐标轴['scale']), self.center_y + self.坐标轴['long']
            else:
                x, y, x2, y2 = self.center_x + self.坐标轴['long'], self.center_y + (i * self.坐标轴['scale']), \
                               self.center_x - self.坐标轴['long'], self.center_y + (i * self.坐标轴['scale'])
            self.坐标点[name][i] = shapes.Line(x=x, y=y, x2=x2, y2=y2, width=3,
                                            color=(41, 123, 203),
                                            batch=self.坐标轴['batch'])
            self.坐标点[name][i].opacity = self.坐标轴['point_opacity']

    def 加载坐标点(self, flush: bool = False):
        if 'scale_x' in self.坐标轴:
            if flush or self.center_x // self.坐标轴['scale'] != self.坐标轴['scale_x']:
                # 如果坐标轴的缩放比例发生变化 或者坐标轴的位置发生变化 或窗口长度发生变化
                self.坐标轴['scale_x'] = self.center_x // self.坐标轴['scale']
                self.加载坐标轴上的点('x')
        else:
            self.坐标轴['scale_x'] = self.center_x // self.坐标轴['scale']
            self.加载坐标轴上的点('x')
        if 'scale_y' in self.坐标轴:
            if flush or self.center_y // self.坐标轴['scale'] != self.坐标轴['scale_y']:
                self.坐标轴['scale_y'] = self.center_y // self.坐标轴['scale']
                self.加载坐标轴上的点('y')
        else:
            self.坐标轴['scale_y'] = self.center_y // self.坐标轴['scale']
            self.加载坐标轴上的点('y')

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

    def on_draw(self):
        self.clear()
        self.back_ground.draw()
        self.draw_batch()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.fps_label.y = height - 10
        self.center_x = width // 2
        self.center_y = height // 2
        # 刷新坐标轴的位置
        self.坐标轴['x'].position = [0, self.center_y,
                                  self.width, self.center_y]
        self.坐标轴['y'].position = [self.center_x, 0,
                                  self.center_x, self.height]
        # 刷新坐标轴上的点的坐标
        self.坐标轴['scale'] = 60
        self.加载坐标点()
        for x in range(-self.坐标轴['scale_x'], self.坐标轴['scale_x'] + 1):
            self.坐标点['x'][x].position = (x * self.坐标轴['scale'] + self.center_x, self.center_y - 5,
                                         x * self.坐标轴['scale'] + self.center_x, self.center_y + 5)
        for y in range(-self.坐标轴['scale_y'], self.坐标轴['scale_y'] + 1):
            self.坐标点['y'][y].position = (self.center_x - 5, y * self.坐标轴['scale'] + self.center_y,
                                         self.center_x + 5, y * self.坐标轴['scale'] + self.center_y)
        # 刷新加载出来的图片的坐标
        if 'textures' in self.runtime:
            self.runtime['textures'].position = (self.center_x - (self.runtime['textures'].width / 2),
                                                 self.center_y - (self.runtime['textures'].height / 2))

    def draw_batch(self):
        self.part_batch.draw()
        self.label_batch.draw()
        if 'textures' in self.runtime:
            self.坐标轴['batch'].draw()

    def load_textures(self, path: str):
        try:
            image = pyglet.image.load(path)
            x = self.center_x - (image.width / 2)
            y = self.center_y - (image.height / 2)
            self.runtime['textures'] = pyglet.sprite.Sprite(x=x, y=y,
                                                            img=image, batch=self.part_batch)
            del image
        except FileNotFoundError:
            self.logger.error(tr.lang('window', 'textures.file_not_found').format(path))

    def load_xml(self, path: str):
        try:
            with open(path, encoding='utf-8') as xml_file:
                xml_json = xmltodict.parse(xml_file.read())
        except FileNotFoundError:
            self.logger.error(tr.lang('window', 'xml.file_not_found').format(path))

    """
    command line event
    """

    def on_command(self, command: line.CommandText):
        self.logger.info(tr.lang('window', 'command.text').format(command))
        if command.match('stop'):
            self.dispatch_event('on_close', 'command')  # source = command
        elif command.match('default'):
            self.set_size(int(self.config_file['window_default']['width']), int(self.config_file['window_default']['height']))
        elif command.match('textures'):
            if command.match('file'):
                name = command.text
                self.load_textures(name)
        elif command.match('set'):
            if command.match('long'):
                self.坐标轴['long'] = int(command)
                self.加载坐标点(True)
            elif command.match('opacity'):
                self.坐标轴['point_opacity'] = int(command)
                self.加载坐标点(True)
            elif command.match('scale'):
                self.坐标轴['scale'] = int(command)
                self.加载坐标点(True)

    def on_message(self, message: line.CommandLine.text):
        self.logger.info(tr.lang('window', 'message.text').format(message))

    def on_file_drop(self, x, y, paths: str):
        f_type = tools.file_type(paths[0])
        if f_type in ('png', 'jpg', 'jpeg'):
            self.load_textures(paths[0])
        self.logger.info(tr.lang('window', 'file.drop').format(paths))

    """
    keyboard and mouse input
    """

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers) -> None:
        pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.logger.debug(f'{x}, {y}, {scroll_x}, {scroll_y}')
        if 'textures' in self.runtime:
            if self.runtime['textures'].scale > 0.1 and self.runtime['textures'].scale + (scroll_y * 0.1) > 0.1:
                self.runtime['textures'].scale += (scroll_y * 0.1)
            elif scroll_y > 0:
                self.runtime['textures'].scale += (scroll_y * 0.1)
            # 设置self.runtime['textures']的位置
            self.runtime['textures'].position = (self.center_x - (self.runtime['textures'].width / 2),
                                                 self.center_y - (self.runtime['textures'].height / 2))

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        self.logger.debug(tr.lang('window', 'mouse.press').format([x, y], tr.lang('window', 'mouse.{}'.format(mouse.buttons_string(button)))))
        if 'textures' in self.runtime:
            # 在点击的位置添加一个红色的半径为3的圆
            self.坐标轴['point'] = shapes.Circle(x, y, 3, color=(255, 255, 255), batch=self.坐标轴['batch'])
            x = Decimal(x - self.center_x)
            y = Decimal(y - self.center_y)
            scale_x = Fraction(x / self.坐标轴['scale'])
            scale_y = Fraction(y / self.坐标轴['scale'])
            self.logger.info(f'x: {float(scale_x)}|{scale_x.limit_denominator(1000)} y: {float(scale_y)}|{scale_y.limit_denominator(1000)}')

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
        if self.run_input:
            self.run_input = False
        self.save_info()
        super().on_close()
        self.logger.info(tr.lang('window', 'game.end'))
