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

import threading

from Difficult_Rocket import crash


class Threads(threading.Thread):
    def run(self) -> None:
        if crash.record_thread:
            crash.all_thread[self.name] = self
        super(Threads, self).run()
