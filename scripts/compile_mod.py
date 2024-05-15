import argparse
import subprocess
import sys
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # script -py <py_version> (3.8 ~ 3.12)
    parser.add_argument("-py", type=str, help="python version")
    parser.add_argument("-all", help="用所有的python版本编译", action="store_true")

    args = parser.parse_args()

    # 移动到项目根目录
    os.chdir("./mods/dr_game/Difficult_Rocket_rs/src")
    os.chdir("./src")

    subprocess.run(["cargo", "fmt", "--all"])

    os.chdir("../")

    if not args.py:
        if args.all:
            all_version = ("38", "39", "310", "311", "312")
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
