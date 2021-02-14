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
        #  log config
        self.log_config = tools.config('configs/logging.json5')
        self.log_file_config = self.log_config['file']
        self.log_file_handler = logging.FileHandler('logs/%s' % (configs.name_handler(
            self.log_file_config['filename']['main'], self.log_file_config['filename']['formats'])))
        #  logger
        #   all logger
        #   client logger
        self.client_log_config = self.log_config['client']
        self.client_logger = logging.getLogger('client')
        self.client_fmt = logging.Formatter(
            fmt=self.client_log_config['fmt'],
            datefmt=self.client_log_config['date_fmt'])
        self.client_stream_handler = logging.StreamHandler()
        self.client_stream_handler.setLevel(self.client_log_config['level'])
        self.client_stream_handler.setFormatter(self.client_fmt)
        self.client_logger.addHandler(self.client_stream_handler)
        #   server logger
        self.server_log_config = self.log_config['server']
        self.server_logger = logging.getLogger('server')
        self.server_fmt = logging.Formatter(
            fmt=self.server_log_config['fmt'],
            datefmt=self.server_log_config['date_fmt'])
        self.server_stream_handler = logging.StreamHandler()
        self.server_stream_handler.setLevel(self.server_log_config['level'])
        self.server_stream_handler.setFormatter(self.server_fmt)
        self.server_logger.addHandler(self.server_stream_handler)
        #   file logger
        self.log_formatter = logging.Formatter(
            fmt=self.log_file_config['fmt'],
            datefmt=self.log_file_config['date_fmt'])
        # client and server
        self.client = client.RenderThread(
            self.client_logger, self.dicts, self.lists, net_mode='local')
        self.server = server.server(
            self.lists, self.dicts, self.server_logger, net_mode='local')

        # start
        self.client.startGame()
