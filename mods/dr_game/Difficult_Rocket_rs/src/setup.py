import sys
import shutil
from setuptools import setup
from setuptools_rust import Binding, RustExtension, Strip

package_path = "Difficult_Rocket_rs"

setup(
    name="Difficult_Rocket_rs",
    version="0.4.2",
    author="shenjackyuanjie",
    author_email="3695888@qq.com",
    rust_extensions=[
        RustExtension(
            target="Difficult_Rocket_rs.Difficult_Rocket_rs",
            binding=Binding.PyO3,
            rustc_flags=["-Ctarget-cpu=native"],
            strip=Strip.No,
        )
    ],
    zip_safe=False,
)

lib_path = "../lib"
build_path = "build"

if "clean" in sys.argv:
    shutil.rmtree(build_path, ignore_errors=True)
    shutil.rmtree(f"{package_path}.egg-info", ignore_errors=True)
    sys.exit(0)
