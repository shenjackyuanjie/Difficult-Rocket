"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import libs
import multiprocessing as mp

from multiprocessing import Manager as share


class Game():

    def __init__(self):
        self.dics = share().dict()
        self.lists = share().list()
        self.client = libs.libs.client()
        self.server = libs.libs.server()

    def setup(self):
        pass
