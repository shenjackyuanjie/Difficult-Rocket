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

import io
import os
import time
import platform
import traceback
import threading
import multiprocessing
from pathlib import Path
from typing import Optional, Union

# import psutil
# for more system info

#  where the crash report from
#  this can't be crash , or the game will really crash!

import Difficult_Rocket

Head_message = """# ----- Difficult Rocket Crash Report -----

## Time: {now_time}

## Traceback
"""

Run_message = """\n## Difficult Rocket running status\n"""

DR_configs = """\n### game config\n"""

Process_message = """\n##  Process info\n"""

Thread_message = """\n##  Thread info\n"""

Python_message = """\n##  Python info\n"""

System_message = """\n##  System info\n"""

all_thread = [threading.main_thread()]
all_process = [multiprocessing.current_process()]


def crash_info_handler(info: Optional[str] = None) -> str:
    if not info:
        info = traceback.format_exc().replace('<', '< ')
    format_info = f"<pre>\n{info}</pre>\n"
    format_info.replace('<module>', '< module>')
    return format_info


def markdown_line_handler(string: Optional[Union[str, bool, int, float]], code: bool = False, level: int = 1,
                          end: str = '\n') -> str:
    lvl = '- ' * level
    f_string = string
    if code:
        f_string = f'`{f_string}`'
    return f'{lvl}{f_string}{end}'


def to_code(string: str):
    return f'`{string}`'


def create_crash_report(info: Optional[str] = None) -> None:
    crash_info = crash_info_handler(info)
    if 'crash_report' not in os.listdir('./'):
        os.mkdir('./crash_report')
    date_time = time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime(time.time()))
    filename = f'crash-{date_time}.md'
    cache_stream = io.StringIO()
    try:
        write_cache(cache_stream, crash_info)
        write_info_to_cache(cache_stream)
    finally:
        get_cache = cache_stream.getvalue()
        cache_stream.close()
    with open(f'./crash_report/{filename}', 'w+', encoding='utf-8') as crash_file:
        crash_file.write(get_cache)


def write_cache(cache_stream, crash_info):
    # 开头信息
    cache_stream.write(Head_message.format(now_time=time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime(time.time()))))
    # 崩溃信息
    cache_stream.write(crash_info)


def write_info_to_cache(cache_stream):
    # 运行状态信息
    from Difficult_Rocket import DR_option, DR_runtime
    cache_stream.write(Run_message)
    cache_stream.write(markdown_line_handler(f'DR Version: {Difficult_Rocket.game_version}', level=1))
    cache_stream.write(markdown_line_handler(f'DR language: {DR_runtime.language}', level=1))
    cache_stream.write(markdown_line_handler(f'Running Dir: {Path(os.curdir).resolve()}', level=1))
    cache_stream.write(f"\n{DR_runtime.as_markdown()}")
    cache_stream.write(DR_configs)
    cache_stream.write(f"\n{DR_option.as_markdown()}")
    cache_stream.write(Process_message)
    for process in all_process:
        process: multiprocessing.Process
        cache_stream.write(markdown_line_handler(f'{process.name}', code=True))
        cache_stream.write(markdown_line_handler(f'Ident: {process.ident}', level=2))
        cache_stream.write(markdown_line_handler(f'Running: {process.is_alive()}', level=2))
    # 运行线程信息
    cache_stream.write(Thread_message)
    for thread in all_thread:
        thread: threading.Thread
        cache_stream.write(markdown_line_handler(f'{thread.name}', code=True))
        cache_stream.write(markdown_line_handler(f'order: {all_thread.index(thread)}', level=2))
        cache_stream.write(markdown_line_handler(f'Ident: {thread.ident}', level=2))
        cache_stream.write(markdown_line_handler(f'Daemon: {thread.daemon}', level=2))
        cache_stream.write(markdown_line_handler(f'Running: {thread.is_alive()}', level=2))
    # Python 信息
    cache_stream.write(Python_message)
    cache_stream.write(markdown_line_handler(f'Version: {to_code(platform.python_version())}', level=1))
    cache_stream.write(markdown_line_handler(f'Branch: {to_code(platform.python_branch())}', level=1))
    cache_stream.write(markdown_line_handler(f'Implementation: {to_code(platform.python_implementation())}', level=1))
    cache_stream.write(markdown_line_handler(f'Compiler: {to_code(platform.python_compiler())}', level=1))
    # 电脑系统信息
    cache_stream.write(System_message)
    cache_stream.write(markdown_line_handler(f'System: {to_code(platform.platform())}', level=1))
    cache_stream.write(markdown_line_handler(f'Computer name: {to_code(platform.node())}', level=1))
    cache_stream.write(markdown_line_handler(f'machine: {to_code(platform.machine())}', level=1))
    cache_stream.write(markdown_line_handler(f'processor: {to_code(platform.processor())}', level=1))
    cache_stream.write(markdown_line_handler(f'release: {to_code(platform.release())}', level=1))
    cache_stream.write(markdown_line_handler(f'version: {to_code(platform.version())}', level=1))


if __name__ == '__main__':
    os.chdir('../../')
    try:
        raise FileNotFoundError('abc')
    except FileNotFoundError:
        create_crash_report()
