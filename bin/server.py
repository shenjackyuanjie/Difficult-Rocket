"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""
import logging
import multiprocessing as mp
import os

try:
    from bin import tools
except (ModuleNotFoundError, ImportError, ImportWarning):
    import tools


class server:
    def __init__(self, dev_list, dev_dic, net_mode='local'):
        # father class __init__()
        # mp.Process.__init__(self)
        # logging
        self.logger = logging.getLogger('server')
        # value
        self.process_id = 'Server'
        self.process_name = 'server process'
        # config
        self.config = tools.config('configs/main.config')
        # lang
        self.lang = tools.config('configs/lang/%s.json5' % self.config['runtime']['language'], 'server')
        # share memory
        self.dev_list = dev_list
        self.dev_dic = dev_dic
        self.logger.info('%s' % self.lang['setup.done'])

    def run(self):
        self.logger.info(self.lang['os.pid_is'].format(os.getpid(), os.getppid()))

