"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

from multiprocessing import Manager as share

import bin

import server
import client


class Game():

    def __init__(self):
        self.dics = share().dict()
        self.lists = share().list()
        self.client = client.RenderThread(self.lists, self.dics, net_mode='local')
        self.server = server.server(self.lists, self.dics, net_mode='local')

    def setup(self):
        pass
