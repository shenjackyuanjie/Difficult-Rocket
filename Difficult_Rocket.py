"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""
import os
import sys
import traceback
import threading
import multiprocessing

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
    # 输出一遍大部分文件位置相关信息 以后可能会加到logs里
    os.chdir(sys.path[0])
    sys.path.append('./Difficult_Rocket')
    sys.path.append('./libs')
    print(sys.path)
    print(hi)

    DEBUGGING = False
    from Difficult_Rocket.api.Exp import *
    # multiprocessing.set_start_method('fork', True)
    print(multiprocessing.get_start_method())
    try:
        from Difficult_Rocket import crash
        from Difficult_Rocket import main

        game = main.Game()
        game.start()

        if DEBUGGING:
            raise TestError('debugging')
    except TestError:
        print('the game is debugging. this crash is raise by TestError')
        error = traceback.format_exc()
        print(error)
        crash.create_crash_report(error)
    except:
        print('the game has unknown error , now outputting error message')
        error = traceback.format_exc()
        print(error)
        crash.create_crash_report(error)
    else:
        crash.record_thread = False
        print(crash.all_thread)
        print(crash.all_process)
        sys.exit(1)
