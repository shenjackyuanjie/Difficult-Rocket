"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import pyglet
import libs

from pyglet.app import run
from pyglet.window import Window


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

    def setup(self):
        # dic
        self.window_c = libs.loads.config(".\\configs\\window.json")
        # window
        self.window = Window(width=int(self.window_c['width']), 
                             height=int(self.window_c['height']),
                             fullscreen=bool(self.window_c['fullscreen']),
                             caption=str(self.window_c['caption']),
                             visible=bool(self.window_c['visible']))
