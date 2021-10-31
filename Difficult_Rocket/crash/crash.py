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
import time
import platform
import traceback
import threading
import multiprocessing
from typing import Optional

# import psutil
# for more system info

#  where the crash report from
#  this can't be crash , or the game will really crash!

# TODO 写完它

Head_message = """# ----- Difficult Rocket Crash Report -----
## Traceback
"""

Process_message = """##  Process info
"""

Thread_message = """##  Thread info
"""

Python_message = """##  Python info
"""

System_message = """##  System info
"""

all_thread = [threading.main_thread()]
all_process = [multiprocessing.current_process()]
record_thread = True


def crash_info_handler(info: str = None) -> str:
    if not info:
        info = traceback.format_exc()
    format_info = f"<pre>\n{info}</pre>\n"
    return format_info


def markdown_line_handler(string: Optional[str or bool or int or float], code: bool = False, level: int = 1, end: str = '\n') -> str:
    lvl = '- ' * level
    f_string = string
    if code:
        f_string = '`{}`'.format(f_string)
    return '{}{}{}'.format(lvl, f_string, end)


def create_crash_report(info: str = None) -> None:
    crash_info = crash_info_handler(info)
    if 'crash_report' not in os.listdir('./'):
        os.mkdir('./crash_report')
    date_time = time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime(time.time()))
    filename = 'crash-{}.md'.format(date_time)
    with open('./crash_report/{}'.format(filename), 'w+', encoding='utf-8') as crash_file:
        # 开头信息
        crash_file.write(Head_message)
        # 崩溃信息
        crash_file.write(crash_info)
        # 多进程信息
        crash_file.write(Process_message)
        for process in all_process:
            process: multiprocessing.Process
            crash_file.write(markdown_line_handler(f'{process.name}', code=True))
            crash_file.write(markdown_line_handler(f'Ident: {process.ident}', level=2))
            crash_file.write(markdown_line_handler(f'Running: {process.is_alive()}', level=2))
        # 运行线程信息
        crash_file.write(Thread_message)
        for thread in all_thread:
            thread: threading.Thread
            crash_file.write(markdown_line_handler(f'{thread.name}', code=True))
            crash_file.write(markdown_line_handler(f'order: {all_thread.index(thread)}', level=2))
            crash_file.write(markdown_line_handler(f'Ident: {thread.ident}', level=2))
            crash_file.write(markdown_line_handler(f'Daemon: {thread.isDaemon()}', level=2))
            crash_file.write(markdown_line_handler(f'Running: {thread.is_alive()}', level=2))
        # Python 信息
        crash_file.write(Python_message)
        crash_file.write(markdown_line_handler(f'Version: {platform.python_version()}', code=True, level=1))
        # crash_file.write(markdown_line_handler(f'Version tuple: {platform.python_version_tuple()}', code=True, level=1))
        # crash_file.write(markdown_line_handler(f'Build: {platform.python_build()}', code=True, level=1))
        crash_file.write(markdown_line_handler(f'Implementation: {platform.python_implementation()}', code=True, level=1))
        crash_file.write(markdown_line_handler(f'Compiler: {platform.python_compiler()}', code=True, level=1))
        # 电脑系统信息
        crash_file.write(System_message)
        crash_file.write(markdown_line_handler(f'System: {platform.platform()}', code=True, level=1))
        crash_file.write(markdown_line_handler(f'Computer name: {platform.node()}', code=True, level=1))
        crash_file.write(markdown_line_handler(f'machine: {platform.machine()}', code=True, level=1))
        crash_file.write(markdown_line_handler(f'processor: {platform.processor()}', code=True, level=1))
        crash_file.write(markdown_line_handler(f'release: {platform.release()}', code=True, level=1))
        crash_file.write(markdown_line_handler(f'version: {platform.version()}', code=True, level=1))


if __name__ == '__main__':
    os.chdir('../')
    try:
        raise FileNotFoundError('abc')
    except:
        create_crash_report()
