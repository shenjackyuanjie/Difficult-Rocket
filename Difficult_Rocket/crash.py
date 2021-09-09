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


import os
import threading
import time
import traceback
from typing import Optional

#  where the crash report from
#  this can't be crash , or the game will really crash!

# TODO 写完它

Head_message = """# ----- Difficult Rocket Crash Report -----
## Traceback
"""

Thread_message = """##  Thread info
"""

System_message = """##  System info
"""

all_thread = [threading.main_thread()]
record_thread = True


def crash_info_handler(info: str = None) -> str:
    if not info:
        info = traceback.format_exc()
    format_info = '- {}'.format(info.replace('\n', '\n- '))
    if (format_info.rfind('- ') + 2) == len(format_info):
        format_info = format_info[:-2]
    return format_info


def markdown_line_handler(string: Optional[str or bool or int or float], code: bool = False, level: int = 1) -> str:
    lvl = '- ' * level
    f_string = string
    if code:
        f_string = '`{}`'.format(f_string)
    return '{}{}\n'.format(lvl, f_string)


def create_crash_report(info: str = None) -> None:
    if info:
        crash_info = crash_info_handler(info)
    else:
        crash_info = crash_info_handler(traceback.format_exc())
    if 'crash_report' not in os.listdir('./'):
        os.mkdir('./crash_report')
    date_time = time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime(time.time()))
    filename = 'crash-{}.md'.format(date_time)
    with open('./crash_report/{}'.format(filename), 'w+') as crash_file:
        crash_file.write(Head_message)  # 开头信息
        crash_file.write(crash_info)
        crash_file.write(Thread_message)
        for thread in all_thread:
            thread: threading.Thread
            crash_file.write(markdown_line_handler(f'{thread.name}', code=True))
            crash_file.write(markdown_line_handler(f'order: {all_thread.index(thread)}', level=2))
            crash_file.write(markdown_line_handler(f'Ident: {thread.ident}', level=2))
            crash_file.write(markdown_line_handler(f'Daemon: {thread.isDaemon()}', level=2))
            crash_file.write(markdown_line_handler(f'Running: {thread.is_alive()}', level=2))
        crash_file.write(System_message)


if __name__ == '__main__':
    os.chdir('../')
    try:
        raise FileNotFoundError('abc')
    except:
        create_crash_report()
