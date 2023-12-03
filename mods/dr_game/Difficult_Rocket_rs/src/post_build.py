#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import os
import shutil
import warnings
import traceback
from pathlib import Path

package_path = "Difficult_Rocket_rs"
lib_path = Path("../lib").resolve()
build_path = "build"

if not os.path.exists(lib_path):
    os.mkdir(lib_path)

builds = os.listdir(build_path)
print(os.path.abspath("."))

try:
    shutil.copy("src/__init__.py", os.path.join(lib_path, "__init__.py"))
except shutil.SameFileError:
    traceback.print_exc()

for build_dir in builds:
    if not os.path.exists(os.path.join(build_path, build_dir, package_path)):
        warnings.warn(f"package not found at {build_path}/{build_dir}")
        continue
    for file in os.listdir(os.path.join(build_path, build_dir, package_path)):
        file_name = os.path.join(lib_path, file)
        shutil.rmtree(file_name, ignore_errors=True)
        try:
            shutil.copy(
                os.path.join(build_path, build_dir, package_path, file), file_name
            )
        except (shutil.SameFileError, PermissionError):
            # print(os.path.exists(os.path))
            print(os.listdir(lib_path))
            traceback.print_exc()
            continue
        print(os.path.abspath(file_name))
