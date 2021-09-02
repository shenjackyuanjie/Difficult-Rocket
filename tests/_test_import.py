"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import importlib

name = 'import_test'

na = importlib.import_module(name)
print(na.__name__)
pllist = {}

pllist[name] = na
pllist[name].a()
