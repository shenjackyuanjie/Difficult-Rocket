#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import os
import time
# import multiprocessing

from Difficult_Rocket.utils import tools
from Difficult_Rocket.utils.translate import tr

from lib_not_dr import loggers


# TODO 改变服务端启动逻辑 0.6.0(划掉 0.8.0)会写完的（


class Server:
    def __init__(self, net_mode="local"):
        start_time = time.time()
        # logging
        self.logger = loggers.config.get_logger("server")
        self.logger.info(tr().server.setup.start())
        # value
        self.process_id = os.getpid()
        # os.set
        self.process_name = "server process"
        # config
        self.config = tools.load_file("config/main.toml")
        # self.dev = Dev
        # self.net_mode = net_mode
        self.logger.info(tr().server.setup.use_time().format(time.time() - start_time))

    def run(self):
        self.logger.info(tr().server.os.pid_is().format(os.getpid(), os.getppid()))

    def __repr__(self):
        return f"<Server {self.process_name} {self.process_id}>"
