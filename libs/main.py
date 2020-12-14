"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import libs
import pyglet
import threading

from pyglet.app import run
from pyglet.window import Window
from pyglet.resource import image


def mbool(thing):  # stand for my bool
    if (thing == "True") or (thing == 1) or (thing == "1"):
        return True
    elif (thing == "False") or (thing == 0) or (thing == "0"):
        return False
    else:
        raise ValueError("Need a 'like bool' not anything else")


class Game():
    def __init__(self):
        pass


class RenderThread(threading.Thread):
    def __init__(self,):
        # value
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
            ".\\configs\\window.json")  # stand for window config
        self.planet_c = libs.loads.config(
            ".\\configs\\planet.json")  # stand for planet config
        self.textures_c = libs.loads.config(
            ".\\configs\\basic_config", "textures")  # stand for textures config
        # image
        self.b_g = image("back_ground_space.png")
        # window
        self.window = Window(width=int(self.window_c['width']),
                             height=int(self.window_c['height']),
                             fullscreen=mbool(self.window_c['fullscreen']),
                             caption=str(self.window_c['caption']),
                             visible=mbool(self.window_c['visible']))

    def on_draw(self):
        pass