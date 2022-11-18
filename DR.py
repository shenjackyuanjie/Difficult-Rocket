# -*- coding: utf-8 -*-
"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""
import os
import sys
import time
import cProfile
import traceback

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
    start_time_ns = time.time_ns()
    start_time_perf_ns = time.perf_counter_ns()
    print(f'{__file__=}')
    print(f'{sys.path[0]=}')
    print(f'{sys.argv[0]=}')
    print(f'{os.getcwd()=}')
    print(f'{os.path.abspath(__file__)=}')
    print(f'{os.path.realpath(__file__)=}')
    print(f'{os.path.split(os.path.split(os.path.realpath(__file__))[0])=}')
    # 输出一遍大部分文件位置相关信息 以后可能会加到logs里
    file_path = os.path.split(os.path.realpath(__file__))[0]
    os.chdir(file_path)  # 将运行路径切换到文件位置 防止bug
    sys.path.append(f'{file_path}/Difficult_Rocket')  # 添加local path
    sys.path.append(f'{file_path}/libs')  # 添加 libs path
    print(sys.path)  # 输出路径
    print(hi)  # hi！

    from Difficult_Rocket.exception import TestError
    from Difficult_Rocket.crash import crash
    from Difficult_Rocket import DR_option
    try:
        import pyglet  # 导入pyglet
        pyglet.resource.path = ['/textures/']
        pyglet.resource.reindex()

        from Difficult_Rocket import main, DR_runtime
        DR_runtime.start_time_ns = start_time_ns

        from pyglet.gl import glClearColor  # 调整背景颜色
        glClearColor(0.5, 0.5, 0.5, 0)

        game = main.Game()  # 实例化一个游戏
        print(time.perf_counter_ns() - start_time_perf_ns, (time.perf_counter_ns() - start_time_perf_ns) / (10 ** 9), 'start')  # 输出一下启动用时

        cprofile = False  # 是否使用cprofile
        if cprofile:
            cProfile.run('game.start()', sort='calls')  # 使用 cprofile 启动
        else:
            game.start()  # 直接启动
        if DR_option.crash_report_test:
            raise TestError('debugging')  # debug 嘛，试试crash
    except Exception as exp:  # 出毛病了
        print(error_format['error.happen'])  #
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
