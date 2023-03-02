#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
import sys
import zipfile
import shutil

if sys.platform == "win32":
    os.system('')


def make_zip():
    with zipfile.ZipFile('./build/main.zip', 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as dist_zip:
        for path, sub_paths, sub_files in os.walk('./build/Difficult-Rocket'):
            print(f'writing {path}')
            for file in sub_files:
                file_path = os.path.join(path, file)
                dist_zip.write(file_path)


def remove_un_use():
    un_use_file = [
        './libs/fonts/Fira_Code',
        './libs/fonts/scientifica'
        './libs/fonts/Monocraft.otf',
        './libs/fonts/SmileySans-Oblique.ttf'
        './libs/fonts/HarmonyOS_Sans/HarmonyOS_Sans_Condensed',
        './libs/fonts/HarmonyOS_Sans/HarmonyOS_Sans'
    ]
    # 删除不必要的文件
    # 如果忽略不存在或无法删除的文件
    os.chdir('./build/Difficult-Rocket')
    for file in un_use_file:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
        except PermissionError:
            pass
    os.chdir('../../')


def copy_data_file():
    files = {
        './libs/pyglet': './build/pyglet',
        './libs/Difficult_Rocket_rs/lib': './build/libs/Difficult_Rocket_rs/lib',
    }
    # 使用 shutil 复制文件
    for src, dist in files.items():
        shutil.copytree(src, dist)


if __name__ == '__main__':
    print(os.listdir('./build'))
    remove_un_use()
    copy_data_file()
    make_zip()
