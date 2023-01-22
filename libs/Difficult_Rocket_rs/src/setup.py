#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import os
import sys
import shutil
import warnings
from setuptools import setup
from setuptools_rust import Binding, RustExtension

sys.path.append('../../../')
if '../../../' in sys.path:
    from Difficult_Rocket import DR_runtime

package_path = 'Difficult_Rocket_rs'

setup(
    name='Difficult_Rocket_rs',
    version=DR_runtime.DR_Rust_version.__str__(),
    author='shenjackyuanjie',
    author_email='3695888@qq.com',
    rust_extensions=[RustExtension(target="Difficult_Rocket_rs.Difficult_Rocket_rs",
                                   # rust_version='2021',
                                   binding=Binding.PyO3)],
    zip_safe=False
)

lib_path = '../lib'
build_path = './build'

if 'clean' in sys.argv:
    shutil.rmtree(lib_path, ignore_errors=True)
    shutil.rmtree(build_path, ignore_errors=True)
    shutil.rmtree(f'{package_path}.egg-info', ignore_errors=True)
    sys.exit(0)

if not os.path.exists(lib_path):
    os.mkdir(lib_path)

builds = os.listdir(build_path)
print(os.path.abspath('.'))

for build_dir in builds:
    if not os.path.exists(os.path.join(build_path, build_dir, package_path)):
        warnings.warn(f'package not found at {build_path}/{build_dir}')
        continue
    for file in os.listdir(os.path.join(build_path, build_dir, package_path)):
        # file_name = os.path.join(lib_path, file.replace(package_path, f'{package_path}.{DR_runtime.DR_Rust_version}'))
        file_name = os.path.join(lib_path, file)
        shutil.rmtree(file_name, ignore_errors=True)
        shutil.copy(os.path.join(build_path, build_dir, package_path, file), file_name)
    # shutil.rmtree(os.path.join(build_path, build_dir))
    # print(os.path.join(build_path, build_dir))
