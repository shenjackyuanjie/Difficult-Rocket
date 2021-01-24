"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import multiprocessing as mp


class server(mp.Process):
    def __init__(self, dev_list, dev_dic):
        # father class __init__()
        mp.Process.__init__(self)
        # value
        self.process_id = 'Server'
        self.process_name = 'server process'
        # share memery
        self.dev_list = dev_list
        self.dev_dic = dev_dic

    def run(self):
        pass
