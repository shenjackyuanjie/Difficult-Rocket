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
import logging

if __name__ == '__main__':  # been start will not run this
    sys.path.append('/bin/libs')
    sys.path.append('/bin')

from Difficult_Rocket.utils import tools
from Difficult_Rocket.utils.translate import tr
from Difficult_Rocket.api.delivery import Delivery
from Difficult_Rocket.utils.new_thread import new_thread


# TODO 改变服务端启动逻辑 0.6.0会写完的（


class Server:
    def __init__(self, net_mode='local', Dev: Delivery = Delivery):
        # father class __init__()
        # mp.Process.__init__(self)
        # logging
        self.logger = logging.getLogger('server')
        # value
        self.process_id = 'Server'
        self.process_name = 'server process'
        # config
        self.config = tools.load_file('configs/main.config')
        self.dev = Dev
        self.net_mode = net_mode
        self.logger.info(tr.lang('server', 'setup.done'))

    def run(self):
        self.logger.info(tr.lang('server', 'os.pid_is').format(os.getpid(), os.getppid()))
