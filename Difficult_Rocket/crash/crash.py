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
from typing import Optional, TextIO

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

Run_message = """\n## Difficult Rocket running status\n"""

DR_configs = """\n### game config\n"""

Process_message = """\n##  Process info\n"""

Thread_message = """\n##  Thread info\n"""

Python_message = """\n##  Python info\n"""

System_message = """\n##  System info\n"""

all_thread = [threading.main_thread()]
all_process = [multiprocessing.current_process()]


def crash_info_handler(info: str = None) -> str:
    if not info:
        info = traceback.format_exc().replace('<', '< ')
    format_info = f"<pre>\n{info}</pre>\n"
    format_info.replace('<module>', '< module>')
    return format_info


def markdown_line_handler(string: Optional[str or bool or int or float], code: bool = False, level: int = 1, end: str = '\n') -> str:
    lvl = '- ' * level
    f_string = string
    if code:
        f_string = f'`{f_string}`'
    return f'{lvl}{f_string}{end}'


def to_code(string: str):
    return f'`{string}`'


def write_markdown_tablet(crash_file: TextIO, tablet: list) -> None:
    a_len = max(tablet[1], 6)
    b_len = max(tablet[2], 5)
    c_len = max(tablet[3], 10)
    crash_file.write(f'\n| Option{" " * (a_len - 4)} | Value{" " * (b_len - 3)} | Value Type{" " * (c_len - 8)} |\n')
    crash_file.write(f'|:{"-" * (a_len + 3)}|:{"-" * (b_len + 3)}|:{"-" * (c_len + 3)}|\n')
    for a, b, c in tablet[0]:
        b, c = str(b), str(c)
        crash_file.write(f'| `{a}`{" " * (a_len - len(a))} | `{b}`{" " * (b_len - len(b))} | `{c}`{" " * (c_len - len(c))} |\n')


def create_crash_report(info: str = None) -> None:
    crash_info = crash_info_handler(info)
    if 'crash_report' not in os.listdir('./'):
        os.mkdir('./crash_report')
    date_time = time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime(time.time()))
    filename = f'crash-{date_time}.md'
    cache_stream = io.StringIO()
    try:
        _extracted_from_create_crash_report_10(cache_stream, crash_info)
    finally:
        get_cache = cache_stream.getvalue()
        cache_stream.close()
    with open(f'./crash_report/{filename}', 'w+', encoding='utf-8') as crash_file:
        crash_file.write(get_cache)


# TODO Rename this here and in `create_crash_report`
def _extracted_from_create_crash_report_10(cache_stream, crash_info):
    # 开头信息
    cache_stream.write(Head_message.format(now_time=time.strftime('%Y/%m/%d %H:%M:%S', time.gmtime(time.time()))))
    # 崩溃信息
    cache_stream.write(crash_info)
    # 运行状态信息
    from Difficult_Rocket import DR_option, DR_runtime
    cache_stream.write(Run_message)
    cache_stream.write(markdown_line_handler(f'DR Version: {Difficult_Rocket.game_version}', level=1))
    cache_stream.write(markdown_line_handler(f'DR language: {DR_runtime.language}', level=1))
    cache_stream.write(markdown_line_handler(f'Running Dir: {Path(os.curdir).resolve()}', level=1))
    option_with_len = (
        _extracted_from__extracted_from_create_crash_report_10_19(
            DR_runtime, cache_stream, DR_configs
        )
    )
    option_with_len = (
        _extracted_from__extracted_from_create_crash_report_10_19(
            DR_option, cache_stream, Process_message
        )
    )
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


# TODO Rename this here and in `create_crash_report`
def _extracted_from__extracted_from_create_crash_report_10_19(arg0, cache_stream, arg2):
    result = arg0.option_with_len()
    write_markdown_tablet(crash_file=cache_stream, tablet=result)
        # # DR 的游戏设置
    cache_stream.write(arg2)
    return result


if __name__ == '__main__':
    os.chdir('../../')
    try:
        raise FileNotFoundError('abc')
    except FileNotFoundError:
        create_crash_report()
