"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import libs
import pyglet
import threading

from threading import Thread

from pyglet.app import run
from pyglet.window import Window
from pyglet.resource import image


class RenderThread(threading.Thread, pyglet.window.Window):

    def __init__(self, thread_ID, thread_name, delivery_class):
        # father class __init__()
        Window.__init__(self)
        threading.Thread.__init__(self)
        # value
        self.thread_id = thread_ID
        self.thread_name = thread_name
        # dic
        self.parts = {}  # this ship parts
        self.o_parts = {}  # stand for opther parts
        self.b_g_e = {}  # stand for back ground element
        self.planet_system = {}  # hole planet system
        # list

    def start_game(self):
        run()
        return

    def setup(self):
        # dic
        self.window_c = libs.loads.config(
            ".\\sys_value\\window.json")  # stand for window config
        self.planet_c = libs.loads.config(
            ".\\sys_value\\planet.json")  # stand for planet config
        self.textures_c = libs.loads.config(
            ".\\sys_value\\basic_config", "textures")  # stand for textures config
        # image
        self.b_g = image("back_ground_space.png")
        # window
        self.window = Window(width=int(self.window_c['width']),
                             height=int(self.window_c['height']),
                             fullscreen=libs.tools.mbool(
                                 self.window_c['fullscreen']),
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
