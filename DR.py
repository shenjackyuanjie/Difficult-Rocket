"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""
import os
import sys
import traceback
import threading
import multiprocessing

# TODO 默认位置配置文件
# TODO 可自定义工作路径


hi = """Difficult Rocket is writen by shenjackyuanjie
mail: 3695888@qq.com or shyj3695888@163.com
QQ: 3695888"""

error_format = {
    'TestError':      '游戏正在调试中，某处引发了一个 TestError，不是bug造成的原因',
    'AssertionError': '游戏的某处检查未通过，情报告issue',
    'error.unknown':  '游戏报错了，现在输出报错信息，请报告issue',
    'error.happen':   '游戏出现了一个报错！正在处理'
}

if __name__ == '__main__':
    print(f'{__file__=}')
    print(f'{sys.path[0]=}')
    print(f'{sys.argv[0]=}')
    print(f'{os.getcwd()=}')
    print(f'{os.path.abspath(__file__)=}')
    print(f'{os.path.realpath(__file__)=}')
    # 输出一遍大部分文件位置相关信息 以后可能会加到logs里
    file_path = os.path.split(os.path.realpath(__file__))[0]
    os.chdir(file_path)
    sys.path.append(f'{file_path}/Difficult_Rocket')
    sys.path.append(f'{file_path}/libs')
    print(sys.path)
    print(hi)

    DEBUGGING = False
    from SRtool.api.Exp import *

    try:
        from SRtool.crash import crash
        from SRtool import main

        game = main.Game()
        game.start()

        if DEBUGGING:
            raise TestError('debugging')
    except Exception as exp:
        from SRtool.translate import tr

        print(error_format['error.happen'])
        error = traceback.format_exc()
        name = type(exp).__name__
        if name in error_format:
            print(error_format[name])
        else:
            print(error_format['error.unknown'])
        print(error)
        crash.create_crash_report(error)
    else:
        crash.record_thread = False
        print(crash.all_thread)
        print(crash.all_process)
