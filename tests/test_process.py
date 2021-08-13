"""
writen by shenjackyuanjie
mail: 3695888@qq.com
github: @shenjackyuanjie
"""
from multiprocessing import Process
import os


def testsss(a):
    print(os.getpid())
    print(os.getppid())


if __name__ == '__main__':
    print(os.getpid())
    print(os.getppid())
    pro = Process(target=testsss, args=('a',))
    pro.start()
    pro.join()


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def f(name):
    info('function f')
    print('hello', name)


if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
