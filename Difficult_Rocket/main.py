"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import logging
import os
import sys
import time
from multiprocessing import Manager as share

if __name__ == '__main__':  # been start will not run this
    sys.path.append('/bin/libs')
    sys.path.append('/bin')

from Difficult_Rocket import client, server
from Difficult_Rocket.libs import pyglet
from Difficult_Rocket.api import tools


class Game:
    def __init__(self):
        # basic config
        self.on_python_v_info = sys.version_info
        self.on_python_v = sys.version.split(' ')[0]
        self.start_time = time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime(time.time()))
        # share memory
        self.dicts = share().dict()
        self.lists = share().list()
        # lang_config
        self.language = tools.config('configs/sys_value/basic_config.json5')
        self.language = self.language['language']
        self.lang = tools.config('configs/lang/%s.json5' % self.language, 'main')
        # logger
        self.log_config = tools.config('configs/logging.json5', 'file')
        self.log_filename = tools.name_handler(self.log_config['filename']['main'],
                                               {'{date}': self.log_config['date_fmt']})
        self.root_logger_fmt = logging.Formatter(self.log_config['fmt'], self.log_config['date_fmt'])
        self.root_logger_stream_handler = logging.StreamHandler()
        self.root_logger_stream_handler.setFormatter(self.root_logger_fmt)
        self.root_logger_stream_handler.setLevel(tools.log_level(self.log_config['level']))
        try:
            self.root_logger_file_handler = logging.FileHandler('logs/' + self.log_filename, encoding='utf-8')
        except FileNotFoundError:
            os.mkdir('./logs')
            self.root_logger_file_handler = logging.FileHandler('logs/' + self.log_filename, encoding='utf-8')
        self.root_logger_file_handler.setFormatter(self.root_logger_fmt)
        self.root_logger_file_handler.setLevel(tools.log_level(self.log_config['level']))
        # root logger setup
        logging.getLogger().setLevel(tools.log_level(self.log_config['level']))
        logging.getLogger().addHandler(self.root_logger_stream_handler)
        logging.getLogger().addHandler(self.root_logger_file_handler)
        # create logger
        self.main_logger = logging.getLogger('main')
        # output info
        self.main_logger.info(self.lang['logger.created'])
        self.main_logger.info(self.lang['logger.main_done'])
        self.log_configs()
        # version check
        self.python_version_check()
        self.setup()

    def setup(self) -> None:
        self.client = client.Client(self.lists, self.dicts, net_mode='local')
        self.server = server.Server(self.lists, self.dicts, net_mode='local')

    def log_configs(self) -> None:
        self.main_logger.info('%s %s' % (self.lang['logger.language'], self.lang['lang.language']))
        self.main_logger.info('%s %s' % (self.lang['game_start.at'], self.start_time))
        self.main_logger.debug('%s %s' % (self.lang['logger.logfile_name'], self.log_filename))
        self.main_logger.debug('%s %s' % (self.lang['logger.logfile_level'], self.log_config['level']))
        self.main_logger.debug('%s %s' % (self.lang['logger.logfile_fmt'], self.log_config['fmt']))
        self.main_logger.debug('%s %s' % (self.lang['logger.logfile_datefmt'], self.log_config['date_fmt']))

    def python_version_check(self) -> None:  # best 3.8+ and write at 3.8.10
        self.main_logger.info('%s %s' % (self.lang['version.now_on'], self.on_python_v))
        if self.on_python_v_info[0] == 2:
            self.main_logger.critical('%s' % self.lang['version.need3+'])
            raise SystemError('%s' % self.lang['version.need3+'])
        elif self.on_python_v_info[1] < 8:
            warning = tools.name_handler(self.lang['version.best3.8+'])
            self.main_logger.warning(warning)

    # @new_thread('main')
    def _start(self) -> int:
        self.server.run()
        try:
            pyglet.app.run()
        except:
            return -1
        else:
            return 1

    def start(self) -> None:
        self._start()
