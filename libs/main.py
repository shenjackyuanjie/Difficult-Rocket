"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

from multiprocessing import Manager as share

import libs


class Game():

    def __init__(self):
        self.dics = share().dict()
        self.lists = share().list()
        self.client = libs.libs.client()
        self.server = libs.libs.server()

    def setup(self):
        pass
