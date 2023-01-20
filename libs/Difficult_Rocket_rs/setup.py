#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import os
import shutil
import warnings
from setuptools import setup
from setuptools_rust import Binding, RustExtension

package_path = './Difficult_Rocket_rs'

setup(
    name='Difficult_Rocket_rs',
    version='0.0.0.1',
    rust_extensions=[RustExtension(target="Difficult_Rocket_rs.Difficult_Rocket_rs",
                                   rust_version='2021',
                                   binding=Binding.PyO3)],
    packages=[package_path],
    zip_safe=False
)

lib_path = './lib'
build_path = './build'

if not os.path.exists(lib_path):
    os.mkdir(lib_path)

builds = os.listdir(build_path)

for build_dir in builds:
    if not os.path.exists(os.path.join(build_path, build_dir, package_path)):
        warnings.warn(f'package not found at {build_path}/{build_dir}')
        continue
    for file in os.listdir(os.path.join(build_path, build_dir, package_path)):
        shutil.copy(os.path.join(build_path, build_dir, package_path, file), os.path.join(lib_path, file))
    # shutil.rmtree(os.path.join(build_path, build_dir))
    print(os.path.join(build_path, build_dir))
