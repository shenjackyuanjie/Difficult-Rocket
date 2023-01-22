#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
import sys
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


def remove_dev_usage():
    un_use_fonts = [
        './'
    ]
    ...


if __name__ == '__main__':
    print(os.listdir('./build'))
    make_zip()
