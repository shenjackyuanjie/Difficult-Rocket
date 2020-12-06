"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import pyglet
import libs

from pyglet.app import run
from pyglet.window import Window
from pyglet.resource import image


def mbool(thing): # stand for my bool
    if (thing == "True") or (thing == 1) or (thing == "1"):
        return True
    elif (thing == "False") or (thing == 0) or (thing == "0"):
        return False
    else:
        raise ValueError("Need a 'like bool' not anything else")

class Game:
    def __init__(self):
        # value
        # dic
        self.parts = {}  # now ship parts
        self.o_parts = {}  # stand for opther parts
        self.b_g_e = {}  # stand for back ground element
        # list

    def start_game(self):
        run()
        return

    def setup(self):
        # dic
        self.window_c = libs.loads.config(".\\configs\\window.json")
        self.tc = libs.loads.config(".\\configs\\basic_config", "textures")
        # image
        self.b_g = image("")
        # window
        self.window = Window(width=int(self.window_c['width']), 
                             height=int(self.window_c['height']),
                             fullscreen=mbool(self.window_c['fullscreen']),
                             caption=str(self.window_c['caption']),
                             visible=mbool(self.window_c['visible']))
