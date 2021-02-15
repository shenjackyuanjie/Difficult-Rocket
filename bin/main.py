"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

# share memory
from multiprocessing import Manager as share

import sys
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
        self.start_time = time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime(time.time()))
        # share memory
        self.dicts = share().dict()
        self.lists = share().list()
        # logger
        self.log_config = tools.config('configs/logging.json5', 'file')
        self.log_filename = configs.name_handler(self.log_config['filename']['main'],
                                                 self.log_config['filename']['formats'])
        self.root_logger_fmt = logging.Formatter(self.log_config['fmt'], self.log_config['date_fmt'])
        self.root_logger_stream_handler = logging.StreamHandler()
        self.root_logger_stream_handler.setLevel(self.log_config['level'])
        self.root_logger_stream_handler.setFormatter(self.root_logger_fmt)
        self.root_logger_stream_handler.setLevel(tools.log_level(self.log_config['level']))
        self.root_logger_file_handler = logging.FileHandler(self.log_filename)
        self.root_logger_file_handler.setFormatter(self.root_logger_fmt)
        self.root_logger_file_handler.setLevel(tools.log_level(self.log_config['level']))
        # root logger setup
        logging.getLogger().setLevel(tools.log_level(self.log_config['level']))
        logging.getLogger().addHandler(self.root_logger_stream_handler)
        logging.getLogger().addHandler(self.root_logger_file_handler)
        # create logger
        self.main_logger = logging.getLogger().getChild('main')
        self.server_logger = logging.getLogger().getChild('server')
        self.client_logger = logging.getLogger().getChild('client')
        self.main_logger.info('client logger and server logger done')
        self.python_version_check()
        # client and server
        self.client = client.RenderThread(
            self.client_logger, self.dicts, self.lists, net_mode='local')
        self.server = server.server(
            self.lists, self.dicts, self.server_logger, net_mode='local')
        # //todo log configs

    def python_version_check(self) -> None:
        py_v_info = sys.version_info
        py_v = str('%d.%d.%d' % (py_v_info[0], py_v_info[1], py_v_info[2]))
        self.main_logger.info('Difficult Rocket is running on Python Vision %s' % py_v)
        if py_v_info[0] == 2:
            self.main_logger.critical('Difficult Rocket need Python vision 3+ but not %s ' % py_v)
            raise Exception('Difficult Rocket need python vision 3+ but not %s ' % py_v)
        elif py_v_info[1] <= 7:
            self.main_logger.warning('Difficult is develop in Python version 3.8 \n and you are running on %s may \
            cause error' % py_v)

    def start(self):
        # start
        self.client.startGame()
