"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import os
import sys
import time
import traceback


#  where the crash report from
#  this can't be crash , or the game will really crash!

# TODO 写完它

head_message = """# ========== Difficult Rocket Crash Report =========="""


def create_crash_report(crash_info: str) -> None:
    print(os.listdir('./'))
    if 'crash_report' not in os.listdir('./'):
        os.mkdir('./crash_report')
    date_time = time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime(time.time()))
    filename = 'crash-{}'


if __name__ == '__main__':
    os.chdir('../')
    create_crash_report('ah')
