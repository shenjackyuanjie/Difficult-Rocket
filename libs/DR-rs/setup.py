#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import sys
from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name='Difficult_Rocket_rs',
    version='0.0.0.1',
    rust_extensions=[RustExtension("Difficult_Rocket_rs.Difficult_Rocket_rs", binding=Binding.PyO3)],
    packages=['Difficult_Rocket_rs'],
    zip_safe=False
)

print(sys.platform)
