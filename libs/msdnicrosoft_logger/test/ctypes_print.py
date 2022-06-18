#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

import time
import ctypes


def run_print():
    # 加载dll
    # ctypes.cdll.LoadLibrary('stdio')
    c_print = ctypes.cdll.LoadLibrary('./print.dll')
    c_print.print_it(ctypes.c_wchar_p(u'12啊3'), ctypes.c_wchar_p('\n'))
    c_print.print_it(ctypes.c_wchar_p(u'12啊3'), ctypes.c_wchar_p('\n'))


if __name__ == "__main__":
    run_print()
