"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import libs
import pyglet
import threading
import multiprocessing as mp

import pyglet.app
from pyglet.window import Window
from pyglet.resource import image


class RenderThread(mp.Process, pyglet.window.Window):

    def __init__(self, dev_list, dev_dic):
        # father class __init__()
        Window.__init__(self)
        mp.Process.__init__(self)
        # value
        self.process_id = 'Render'
        self.process_name = 'render process'
        # share memery
        self.dev_list = dev_list
        self.dev_dic = dev_dic
        # dic
        self.parts = {}  # this ship parts
        self.o_parts = {}  # stand for opther parts
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
                             fullscreen=libs.tools.mbool(self.window_c['fullscreen']),
                             caption=str(self.window_c['caption']),
                             visible=libs.tools.mbool(self.window_c['visible']))

    def on_draw(self):
        pass

    def on_mouse_motion(self):
        pass

    def on_key_press(self):
        pass

    def on_key_release(self):
        pass
