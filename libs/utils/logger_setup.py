#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
# import setuptools
from setuptools import setup
from Cython.Build import cythonize
setup(name='logger',
      zip_safe=False,
      ext_modules=cythonize('logger.py', language_level=3))
