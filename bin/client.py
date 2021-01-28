"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import multiprocessing as mp

import bin
import pyglet
import pyglet.app
from pyglet.resource import image
from pyglet.window import Window


class RenderThread(mp.Process, pyglet.window.Window):

    def __init__(self, dev_list, dev_dic, logger, net_mode='local'):
        # do father class __init__()
        Window.__init__(self)
        mp.Process.__init__(self)
        # logging
        self.logger = logger
        # value
        self.process_id = 'Render'
        self.process_name = 'render process'
        # share memory
        self.dev_list = dev_list
        self.dev_dic = dev_dic
        # dic
        self.parts = {}  # this ship parts
        self.o_parts = {}  # stand for other parts
        self.b_g_e = {}  # stand for back ground element
        self.planet_system = {}  # hole planet system
        # list

    def start_game(self):
        pyglet.app.run()
        return

    def setup(self):
        # dic
        # image
        self.b_g = image("back_ground_space.png")
        # window
        self.window = Window(width=int(self.window_c['width']),
                             height=int(self.window_c['height']),
                             fullscreen=bin.tools.mbool(self.window_c['full_screen']),
                             caption=str(self.window_c['caption']),
                             visible=bin.tools.mbool(self.window_c['visible']))

    """
    keyboard and mouse input
    """

    def on_draw(self):
        # render parts
        for part in self.parts:
            pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass
