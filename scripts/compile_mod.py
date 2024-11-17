import os
import sys
import argparse
import subprocess

from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # script -py <py_version> (3.8 ~ 3.13)
    parser.add_argument("-py", type=str, help="python version")
    parser.add_argument("-all", help="用所有的python版本编译", action="store_true")
    parser.add_argument("-clean", help="清理编译文件", action="store_true")

    args = parser.parse_args()

    # 移动到项目根目录
    os.chdir("./mods/dr_game/Difficult_Rocket_rs/src")
    os.chdir("./src")

    subprocess.run(["cargo", "fmt", "--all"])

    if args.clean:
        subprocess.run(["cargo", "clean"])

    os.chdir("../")

    if args.clean:
        subprocess.run([sys.executable, "setup.py", "clean"])

        sys.exit(0)

    if not args.py:
        if args.all:
            all_version = ("38", "39", "310", "311", "312", "313")
            for py_version in all_version:
                try:
                    subprocess.run([f"python{py_version}", "setup.py", "build"])
                except FileNotFoundError:
                    print(f"python{py_version} not found")
        else:
            subprocess.run([sys.executable, "setup.py", "build"])
    else:
        subprocess.run([args.py, "setup.py", "build"])

    # post
    subprocess.run([sys.executable, "post_build.py"])
