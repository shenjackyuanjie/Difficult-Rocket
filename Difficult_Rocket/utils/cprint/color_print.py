import _winapi
import subprocess
import os

os.system('')

reset = '\033[0m'

print('A 000')

do = False


def rgb(r: int, g: int, b:int) -> tuple:
    return 2, r, g, b


# i_list = list(range(30, 39, 1))
# # i_list = [39]
# j_list = list(range(40, 49, 1))
# # j_list = [49]
#
# for i in i_list:
#     for j in j_list:
#         print(f'\033[{i};{j}m{i}|{j} {reset}', end='|')
#     print()
# print()


def color_print(*args):
    args = [str(i) for i in args]
    out = '|'.join(args)
    line = ';'.join(args)
    print(f'\033[{line}m{out}\033[0m')


if os.name == "nt":
    from ctypes import windll
    from ctypes.wintypes import BOOL, HANDLE, WORD

    handle = _winapi.GetStdHandle(_winapi.STD_OUTPUT_HANDLE)
    kernel32 = windll.LoadLibrary("Kernel32.dll")
    SetConsoleAttribute = kernel32.SetConsoleTextAttribute
    SetConsoleAttribute.argtypes = (HANDLE, WORD)
    SetConsoleAttribute.restype = BOOL
    # FOREGROUND_INTENSITY|FOREGROUND_RED
    res: bool = SetConsoleAttribute(handle, 5)
    print(res)
    string = "Hello World!"
    _winapi.WriteFile(handle, string.encode("utf-8"), 0)
else:
    pass

# exit(0)

color_print(94)
color_print(41, 93)
color_print(36, 40)
print()
color_print(48, *rgb(200, 100, 20), 34)
color_print(48, *rgb(255, 161, 72))
color_print(48, *rgb(255, 161, 72), 38, *rgb(1, 50, 255))
color_print(48, *rgb(178, 112, 50), 38, *rgb(98, 96, 167))
print()
color_print(48, *rgb(100, 10, 10), )
exit(0)
