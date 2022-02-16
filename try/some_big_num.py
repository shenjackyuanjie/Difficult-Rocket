#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""
import cProfile


def run():
    一个很大的整数 = 11111111111111111111111111111111111111111111111 * 111111235111

    一个很大的浮点数 = 1111111111111111111111111111111111111111.1111111 * 11111123.5111
    print(一个很大的整数, '\n', 一个很大的浮点数)


cProfile.run("run")

"""
1234569279011111111111111111111111111111111111098765418321 
 1.234569279011111e+46
 """
