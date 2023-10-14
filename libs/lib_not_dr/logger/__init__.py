#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import sys

from lib_not_dr.types.options import Options

COLOR_SUPPORT = True

if sys.platform == "win32":
    try:
        # https://stackoverflow.com/questions/36760127/...
        # how-to-use-the-new-support-for-ansi-escape-sequences-in-the-windows-10-console
        from ctypes import windll

        kernel32 = windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except OSError:  # pragma: no cover
        COLOR_SUPPORT = False


class LogLevel(Options):
    name = 'LogLevel'
    notset: int = 0
    trace: int = 5
    fine: int = 7
    debug: int = 10
    info: int = 20
    warn: int = 30
    error: int = 40
    fatal: int = 50
