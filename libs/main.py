"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import pyglet
import libs

from pyglet.window import Window
from pyglet.app import run


class Game:
    def __init__(self):
        # value
        # dic
        self.parts = {}  # now ship parts
        self.o_parts = {}  # stand for opther parts
        self.b_g_e = {}  # stand for back ground element
        self.window_c = libs.loads.window_config()
        # list

    def start_game(self):
        run()

    def setup(self):
        # window
        self.window = Window(width=800, height=600,
                    caption='minecraft PE', resizable=True)


