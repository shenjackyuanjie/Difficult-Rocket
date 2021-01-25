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
import server
import client

# get time when the program to start the logging
start_time = time.time()
start_time_date = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime(start_time))

# ---------- option start ----------
log_level = logging.DEBUG  # log level


class Game():

    def __init__(self):
        self.start_time = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime(start_time))
        self.dics = share().dict()
        self.lists = share().list()
        self.server_logger = logging.getLogger('server')
        self.client_logger = logging.getLogger('client')
        self.client = client.RenderThread(self.lists, self.dics, self.client_logger, net_mode='local')
        self.server = server.server(self.lists, self.dics, self.server_logger, net_mode='local')
