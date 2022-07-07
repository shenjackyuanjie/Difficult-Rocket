from setuptools import setup, Extension
import shutil
import os

pycprint = Extension('pycprint',
                     sources=['py_cprint.c'])

setup(name='PyCprint',
      version='0.0.1',
      author='shenjack',
      author_email='3695888@qq.com',
      description='这是一个用于直接调用c的printf的库',
      ext_modules=[pycprint])


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
    shutil.copy(os.path.join(build, copy[0]), './')
