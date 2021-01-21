"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

from libs.Game_threads import orbit_demo

import libs
import multiprocessing as mp

from multiprocessing import Manager as share


class Game():

    def __init__(self):
        self.dics = share().dict()
        self.lists = share().list()
        self.render = libs.libs.render_thread.RenderThread(self.lists, self.dics)

    def setup(self):
        self.game_thread = orbit_demo()
