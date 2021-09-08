"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import os
import sys
import traceback
import threading

# TODO 默认位置配置文件+可自定义工作路径


hi = """Difficult Rocket is writen by shenjackyuanjie
mail: 3695888@qq.com or shyj3695888@163.com
QQ: 3695888"""
if __name__ == '__main__':
    print("sys.path[0] = ", sys.path[0])
    print("sys.argv[0] = ", sys.argv[0])
    print("__file__ = ", __file__)
    print("os.path.abspath(__file__) = ", os.path.abspath(__file__))
    print("os.path.realpath(__file__) = ", os.path.realpath(__file__))
    print("os.path.dirname(os.path.realpath(__file__)) = ", os.path.dirname(os.path.realpath(__file__)))
    print("os.path.split(os.path.realpath(__file__)) = ", os.path.split(os.path.realpath(__file__)))
    print("os.path.split(os.path.realpath(__file__))[0] = ", os.path.split(os.path.realpath(__file__))[0])
    print("os.getcwd() = ", os.getcwd())

    os.chdir(sys.path[0])  # TODO 没做完.ing
    sys.path.append('Difficult_Rocket')
    sys.path.append('Difficult_Rocket/libs')

    print(hi)
    try:
        from Difficult_Rocket import main
        from Difficult_Rocket import crash

        game = main.Game()
        game.start()
    except:
        print('the game has error , now outputting error message')
        error = traceback.format_exc()
        print(error)
        from Difficult_Rocket.api import thread

        crash_thread = thread.Threads(target=crash.create_crash_report, args=(error,), name='Crash report thread')
        crash_thread.start()
        crash_thread.join()
    else:
        crash.record_thread = False
        print(crash.all_thread)
