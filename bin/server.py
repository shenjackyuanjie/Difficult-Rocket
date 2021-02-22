"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import os
import multiprocessing as mp

try:
    from bin import tools
except (ModuleNotFoundError, ImportError, ImportWarning):
    import tools


class server(mp.Process):
    def __init__(self, dev_list, dev_dic, logger, language='zh-cn', net_mode='local'):
        # father class __init__()
        mp.Process.__init__(self)
        # logging
        self.logger = logger
        # value
        self.process_id = 'Server'
        self.process_name = 'server process'
        self.process_pid = os.getpid()
        # lang
        self.lang = tools.config('sys_value/lang/%s.json5' % language, 'server')
        # share memory
        self.dev_list = dev_list
        self.dev_dic = dev_dic
        self.logger.info('%s: %s%s' % (self.lang['os.pid_is1'], self.process_pid, self.lang['os.pid_is2']))
        self.logger.info('%s' % self.lang['setup.done'])

    def run(self):
        pass
