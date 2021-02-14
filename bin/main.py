'''
writen by shenjackyuanjie
mail: 3695888@qq.com
'''

# share memory
from multiprocessing import Manager as share

# import bin
import time
import logging

try:
    from bin import tools
    from bin import client
    from bin import server
    from bin import configs
except (ModuleNotFoundError, ImportError, ImportWarning):
    import tools
    import client
    import server
    import configs


class Game:

    def __init__(self):
        # basic config
        self.start_time = time.strftime(
            '%Y-%m-%d %H-%M-%S', time.gmtime(time.time()))
        # share memory
        self.dicts = share().dict()
        self.lists = share().list()
        # logger
        logging.basicConfig(filename='logs/%s.log' % (time.time()))
        self.log_config = tools.config('configs/logging.json5', 'file')
        self.log_filename = 'logs/' + configs.name_handler(
            self.log_config['filename']['main'], self.log_config['filename']['formats'])
        self.log_file_hander = logging.FileHandler(self.log_filename)
        self.log_file_hander.setLevel(tools.log_level(self.log_config['level']))
        self.log_stream_hander = logging.StreamHandler()
        self.log_stream_hander.setLevel(tools.log_level(self.log_config['level']))
        logging.getLogger().addHandler(self.log_stream_hander)
        logging.info('logger done')
        # logging.getLogger().addHandler(self.log_file_hander)
        logging.info('logger done')
        self.server_logger = logging.getLogger()
        self.client_logger = logging.getLogger()
        self.client_logger.info('client logger and server logger done')
        # client and server
        self.client = client.RenderThread(
            self.client_logger, self.dicts, self.lists, net_mode='local')
        self.server = server.server(
            self.lists, self.dicts, self.server_logger, net_mode='local')

        # start
        self.client.startGame()
