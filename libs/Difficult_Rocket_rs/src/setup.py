#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import sys
import shutil
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
    zip_safe=False,
)

lib_path = '../lib'
build_path = 'build'

if 'clean' in sys.argv:
    shutil.rmtree(lib_path, ignore_errors=True)
    shutil.rmtree(build_path, ignore_errors=True)
    shutil.rmtree(f'{package_path}.egg-info', ignore_errors=True)
    sys.exit(0)
