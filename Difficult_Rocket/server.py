#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""


import logging
import os
import sys

if __name__ == '__main__':  # been start will not run this
    sys.path.append('/bin/libs')
    sys.path.append('/bin')

from api import tools
from api.delivery import Delivery
from api.new_thread import new_thread


# TODO 改变服务端启动逻辑 0.6.0会写完的（


class Server:
    def __init__(self, dev_list, dev_dic, net_mode='local', Dev: Delivery = Delivery):
        # father class __init__()
        # mp.Process.__init__(self)
        # logging
        self.logger = logging.getLogger('server')
        # value
        self.process_id = 'Server'
        self.process_name = 'server process'
        # config
        self.config = tools.config('configs/main.config')
        self.dev = Dev
        self.net_mode = net_mode
        # lang
        self.lang = tools.config('configs/lang/%s.json5' % self.config['runtime']['language'], 'server')
        # share memory
        self.dev_list = dev_list
        self.dev_dic = dev_dic
        self.logger.info('%s' % self.lang['setup.done'])

    @new_thread('Server')
    def run(self):
        self.logger.info(self.lang['os.pid_is'].format(os.getpid(), os.getppid()))
        self.logger.debug(self)
