"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

hi = """Difficult Rocket is writen by shenjackyuanjie
mail: 3695888@qq.com or shyj3695888@163.com
QQ: 3695888"""

import os
import sys

## TODO 默认位置配置文件+可自定义工作路径


if __name__ == '__main__':
    print("sys.path[0] = ", sys.path[0])
    print("sys.argv[0] = ", sys.argv[0])
    print("__file__ = ", __file__)
    print("os.path.abspath(__file__) = ", os.path.abspath(__file__))
    print("os.path.realpath(__file__) = ", os.path.realpath(__file__))
    print("os.path.dirname(os.path.realpath(__file__)) = ", 
    os.path.dirname(os.path.realpath(__file__)))
    print("os.path.split(os.path.realpath(__file__)) = ", 
    os.path.split(os.path.realpath(__file__)))
    print("os.path.split(os.path.realpath(__file__))[0] = ", 
    os.path.split(os.path.realpath(__file__))[0])
    print("os.getcwd() = ", os.getcwd())
    from bin import main
    os.chdir(sys.path[0]) # TODO 没做完.ing
    print(hi)
    game = main.Game()
    game.start()