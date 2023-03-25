#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import os
import sys
import rtoml
import shutil
from setuptools import setup
from setuptools_rust import Binding, RustExtension

sys.path.append('../../../')
sys.path.append(os.curdir)

package_path = 'pyglet_rs'

# 版本号从 cargo.toml 中读取
with open(f'Cargo.toml', 'r') as f:
    cargo_toml = rtoml.load(f)
    version = cargo_toml['package']['version']

setup(
    name='pyglet_rs',
    version=version,
    author='shenjackyuanjie',
    author_email='3695888@qq.com',
    rust_extensions=[RustExtension(target="pyglet_rs.pyglet_rs",
                                   binding=Binding.PyO3)],
    zip_safe=False,
)

lib_path = '../lib'
build_path = 'build'

if 'clean' in sys.argv:
    shutil.rmtree(build_path, ignore_errors=True)
    shutil.rmtree(f'{package_path}.egg-info', ignore_errors=True)
    sys.exit(0)
