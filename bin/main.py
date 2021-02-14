"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

# share memory
from multiprocessing import Manager as share

# import bin
import time
import logging

try:
    from bin import tools
    from bin import client
    from bin import server
except (ModuleNotFoundError, ImportError, ImportWarning):
    import tools
    import client
    import server


class Game:

    def __init__(self):
        # basic config
        self.start_time = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime(time.time()))
        self.configs = ''
        # share memory
        self.dicts = share().dict()
        self.lists = share().list()
        # logger
        self.client_logger = logging.getLogger('client')
        self.client_stream_handler = logging.StreamHandler()
        self.server_logger = logging.getLogger('server')
        self.server_stream_handler = logging.StreamHandler()
        self.log_file_handler = logging.FileHandler('')
        self.log_formatter = logging.Formatter("[%(asctime)s][%(name)s]:[%(levelname)s] %(message)s")
        # client and server
        self.client = client.RenderThread(self.client_logger, self.dicts, self.lists, net_mode='local')
        self.server = server.server(self.lists, self.dicts, self.server_logger, net_mode='local')

        # start
        self.client.startGame()
