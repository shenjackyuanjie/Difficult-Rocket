#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name='Difficult_Rocket-rs',
    version='0.0.0.1',
    rust_extensions=[RustExtension("Difficult_Rocket-rs.Difficult_Rocket-rs", binding=Binding.PyO3)],
    packages=['Difficult_Rocket-rs'],
    zip_safe=False
)
