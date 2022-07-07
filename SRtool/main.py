#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import os
import sys
import time
import logging
import logging.config
import multiprocessing

if __name__ == '__main__':  # been start will not run this
    sys.path.append('/bin/libs')
    sys.path.append('/bin')

from SRtool import client
from SRtool.api import tools
from SRtool.translate import tr


class Game:
    def __init__(self):
        # basic config
        self.on_python_v_info = sys.version_info
        self.on_python_v = sys.version.split(' ')[0]
        self.start_time = time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime(time.time()))
        # lang_config
        self.language = tools.load_file('configs/main.config', 'runtime')['language']
        tr.set_language(self.language)
        # logging config
        log_config = tools.load_file('configs/logger.toml')
        file_name = log_config['handlers']['file']['filename']
        del log_config['handlers']['file']['datefmt']
        log_config['handlers']['file']['filename'] = f'logs/{file_name.format(self.start_time)}'
        try:
            logging.config.dictConfig(log_config)
            self.logger = logging.getLogger('main')
        except ValueError:  # it should be no 'logs/' folder
            os.mkdir('logs')
            logging.config.dictConfig(log_config)
            self.logger = logging.getLogger('main')
            self.logger.info(tr['main']['logger.mkdir'])
        self.logger.info(tr['main']['logger.created'])
        # version check
        self.python_version_check()
        self.client = client.Client()


    def python_version_check(self) -> None:  # best 3.8+ and write at 3.8.10
        self.logger.info('%s %s' % (tr['main']['version.now_on'], self.on_python_v))
        if self.on_python_v_info[0] == 2:
            self.logger.critical('%s' % tr['main']['version.need3+'])
            raise SystemError('%s' % tr['main']['version.need3+'])
        elif self.on_python_v_info[1] < 8:
            warning = tools.name_handler(tr['main']['version.best3.8+'])
            self.logger.warning(warning)

    def start(self) -> None:
        self.client.start()
