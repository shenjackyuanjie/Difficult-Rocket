#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
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
import Difficult_Rocket

Head_message = """# ----- Difficult Rocket Crash Report -----
## Time: {now_time}
## Traceback
"""

Run_message = """## Difficult Rocket running status\n"""

DR_configs = """### game config"""

Process_message = """##  Process info\n"""

Thread_message = """##  Thread info\n"""

Python_message = """##  Python info\n"""

System_message = """##  System info\n"""

all_thread = [threading.main_thread()]
all_process = [multiprocessing.current_process()]
record_thread = True


def crash_info_handler(info: str = None) -> str:
    if not info:
        info = traceback.format_exc().replace('<', '< ')
    format_info = f"<pre>\n{info}</pre>\n"
    return format_info


def markdown_line_handler(string: Optional[str or bool or int or float], code: bool = False, level: int = 1, end: str = '\n') -> str:
    lvl = '- ' * level
    f_string = string
    if code:
        f_string = '`{}`'.format(f_string)
    return '{}{}{}'.format(lvl, f_string, end)


def to_code(string: str):
    return '`' + string + '`'


def create_crash_report(info: str = None) -> None:
    crash_info = crash_info_handler(info)
    if 'crash_report' not in os.listdir('./'):
        os.mkdir('./crash_report')
    date_time = time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime(time.time()))
    filename = 'crash-{}.md'.format(date_time)
    with open('./crash_report/{}'.format(filename), 'w+', encoding='utf-8') as crash_file:
        # 开头信息
        crash_file.write(Head_message.format(now_time=time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime(time.time()))))
        # 崩溃信息
        crash_file.write(crash_info)
        # 运行状态信息
        crash_file.write(Run_message)
        crash_file.write(markdown_line_handler(f'DR Version: {Difficult_Rocket.game_version}', level=1))
        crash_file.write(markdown_line_handler(f'Running Dir: {os.path.abspath(os.curdir)}', level=1))
        crash_file.write(markdown_line_handler(f': {os.name=}', level=1))
        crash_file.write(markdown_line_handler(f'DR Version: {str(Difficult_Rocket.Version)}', level=1))
        crash_file.write(markdown_line_handler(f'DR Version: {str(Difficult_Rocket.Version)}', level=1))
        # # DR 的游戏设置
        crash_file.write(DR_configs)
        for key, value in Difficult_Rocket.DR_options.items():
            crash_file.write(markdown_line_handler(f'Option: {to_code(key)} Type: {to_code(Difficult_Rocket.DR_option_type(key))}', level=1))
            crash_file.write(markdown_line_handler(f'Value: {to_code(value)}', level=2))
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
        crash_file.write(markdown_line_handler(f'Version: {to_code(platform.python_version())}', level=1))
        crash_file.write(markdown_line_handler(f'Branch: {to_code(platform.python_branch())}', level=1))
        # crash_file.write(markdown_line_handler(f'Build: {platform.python_implementation()}', code=True, level=1))
        crash_file.write(markdown_line_handler(f'Implementation: {to_code(platform.python_implementation())}', level=1))
        crash_file.write(markdown_line_handler(f'Compiler: {to_code(platform.python_compiler())}', level=1))
        # 电脑系统信息
        crash_file.write(System_message)
        crash_file.write(markdown_line_handler(f'System: {to_code(platform.platform())}', level=1))
        crash_file.write(markdown_line_handler(f'Computer name: {to_code(platform.node())}', level=1))
        crash_file.write(markdown_line_handler(f'machine: {to_code(platform.machine())}', level=1))
        crash_file.write(markdown_line_handler(f'processor: {to_code(platform.processor())}', level=1))
        crash_file.write(markdown_line_handler(f'release: {to_code(platform.release())}', level=1))
        crash_file.write(markdown_line_handler(f'version: {to_code(platform.version())}', level=1))


if __name__ == '__main__':
    os.chdir('../../')
    try:
        raise FileNotFoundError('abc')
    except FileNotFoundError:
        create_crash_report()
