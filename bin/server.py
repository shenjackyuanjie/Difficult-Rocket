'''
writen by shenjackyuanjie
mail: 3695888@qq.com
'''

import multiprocessing as mp


class server(mp.Process):
    def __init__(self, dev_list, dev_dic, logger, language='zh-cn', net_mode='local'):
        # father class __init__()
        mp.Process.__init__(self)
        # logging
        self.logger = logger
        # value
        self.process_id = 'Server'
        self.process_name = 'server process'
        # share memory
        self.dev_list = dev_list
        self.dev_dic = dev_dic
        self.logger.info('server setup done!')

    def run(self):
        pass
