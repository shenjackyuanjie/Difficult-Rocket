"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

from libs import Game_threads
import libs
import pyglet
import threading


class Game():

    def __init__(self):
        pass

    def setup(self):
        self.game_thread = orbit_demo()


test = Game()
test.setup()