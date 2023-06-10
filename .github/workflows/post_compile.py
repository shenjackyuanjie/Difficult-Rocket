#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
import sys
import shutil
import zipfile

if sys.platform == "win32":
    os.system('')


def make_zip():
    with zipfile.ZipFile('./build/main.zip', 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as dist_zip:
        for path, sub_paths, sub_files in os.walk('./build/Difficult-Rocket'):
            print(f'writing {path}')
            for file in sub_files:
                file_path = os.path.join(path, file)
                dist_zip.write(file_path)


def show_files():
    print("----------")
    try:
        print(os.listdir('libs'))
        print(os.listdir('build'))
        print(os.listdir('build/libs'))
        print(os.listdir('build/libs/fonts'))
        print(os.listdir("build/libs/Difficult_Rocket_rs"))
    except Exception as e:
        print(f'list file error {e}')
    print('-----------')


def remove_un_use():
    un_use_file = [
        'libs/fonts/Fira_Code',
        'libs/fonts/scientifica',
        'libs/fonts/Monocraft.otf',
        'libs/fonts/SmileySans-Oblique.ttf',
        'libs/fonts/HarmonyOS_Sans/HarmonyOS_Sans_Condensed',
        'libs/fonts/HarmonyOS_Sans/HarmonyOS_Sans',
    ]
    # 删除不必要的文件
    # 如果忽略不存在或无法删除的文件
    os.chdir('./build/Difficult-Rocket')
    print(os.listdir())
    print(os.path.abspath(os.curdir))
    print("=============")
    for the_file in un_use_file:
        print(f"file: {the_file}")
        try:
            os.remove(the_file)
            shutil.rmtree(the_file, ignore_errors=True)
            print(f"origin remove {the_file}")
        except PermissionError:
            print(f"Permission denied at {os.path.abspath(the_file)}")
        except (IsADirectoryError, FileNotFoundError):
            # 如果是目录
            try:
                shutil.rmtree(the_file)
                print(f"remove dir {os.path.abspath(the_file)}")
            except FileNotFoundError:
                print(f"FileNotFoundError at {os.path.abspath(the_file)}")
        print("=============")
    os.chdir('../../')


def copy_data_file():
    files = {
        'libs/pyglet': 'build/pyglet',
        'libs/Difficult_Rocket_rs/lib': 'build/libs/Difficult_Rocket_rs/lib',
        'libs/fonts': 'build/libs/fonts'
    }
    # 使用 shutil 复制文件
    # os.mkdir("build/pyglet")
    # os.mkdir("build/libs")
    # os.mkdir("build/libs/Difficult_Rocket_rs")
    # os.mkdir("build/libs/Difficult_Rocket_rs/lib")
    for src, dist in files.items():
        try:
            shutil.copytree(src, dist)
        except Exception as e:
            print(f"error: {e}")


if __name__ == '__main__':
    show_files()
    remove_un_use()
    show_files()
    copy_data_file()
    show_files()
    make_zip()
