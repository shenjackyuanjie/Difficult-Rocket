#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import os
import shutil
from setuptools import setup
from Cython.Build import cythonize

setup(name='logger',
      zip_safe=False,
      ext_modules=cythonize('logger.pyx',
                            language_level=3,
                            annotate=True))


def dir_not_temp(path: str):
    return path.find('temp') and os.path.isdir(os.path.join('build', path))


build_dir = os.listdir('./build')
build_dir = list(filter(dir_not_temp, build_dir))
# 用列表推导式把 是文件夹 且 名字里没有 temp 的抽出来
print(build_dir)

os.chdir('build')
# 把运行路径迁移过去，方便copy

for build in build_dir:
    copy = os.listdir(build)
    if not os.path.isdir(build):
        for file in copy:
            shutil.copy(os.path.join(build, file), './')
    else:
        for dirs in copy:
            i = os.listdir(os.path.join(build, dirs))
            for j in i:
                shutil.copy(os.path.join(build, dirs, j), './')

