"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import pyglet
import libs
import sys
import os


def main():
    # Python vision check
    py_v_info = sys.version_info
    py_v = str("%d.%d.%d" % (py_v_info[0], py_v_info[1], py_v_info[2]))
    print("Simple Rocket is running on Python Vision %s" % py_v)
    if py_v_info[0] == 2:
        raise Exception("Simple Rocket need python vision 3+")
    # start games


if __name__ == "__main__":
    main()
