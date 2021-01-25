"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

# share memory
from multiprocessing import Manager as share

import bin
import time
import logging

# 直接导入
import bin.server as server
import bin.client as client


class Game():

    def __init__(self):
        # basic config
        self.start_time = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime(time.time()))
        self.configs = ''
        # share memory
        self.dicts = share().dict()
        self.lists = share().list()
        # logger
        self.server_logger = logging.getLogger('server')
        self.client_logger = logging.getLogger('client')
        self.log_file_handler = logging.FileHandler('')
        # client and server
        self.client = client.RenderThread(self.lists, self.dicts, self.client_logger, net_mode='local')
        self.server = server.server(self.lists, self.dicts, self.server_logger, net_mode='local')
