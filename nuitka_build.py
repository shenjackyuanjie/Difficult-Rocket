#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import os
import sys
import time
import shutil
import tomlkit
import zipfile
import platform
import traceback
import subprocess

from pathlib import Path

from libs.utils import nuitka

if __name__ == '__main__':
    compiler = nuitka.CompilerHelper()

    # 修改 python 执行文件 为 运行时的 python
    compiler.python_cmd = sys.executable

    # 检测 --github 参数
    is_github = False
    if '--github' in sys.argv:
        is_github = True
        compiler.use_ccache = False
        compiler.show_progress = False
        compiler.output_path = Path('./build/github')
        compiler.python_cmd = 'python'
        compiler.include_data_dir.remove(('./libs/fonts', './libs/fonts'))

    # 检测 --output xx 参数
    if '--output' in sys.argv:
        # 输入的是输出目录
        compiler.output_path = sys.argv[sys.argv.index('--output') + 1]
        sys.argv.remove('--output')
        sys.argv.remove(compiler.output_path)

    pyglet_optimizations = True
    if pyglet_optimizations:
        if platform.system() == "Windows":
            compiler.no_follow_import.append('pyglet.libs.darwin')
            compiler.no_follow_import.append('pyglet.libs.x11')
            compiler.no_follow_import.append('pyglet.window.xlib')
            compiler.no_follow_import.append('pyglet.window.cocoa')
            compiler.no_follow_import.append('pyglet.window.headless')
        elif platform.system() == "Darwin":
            compiler.no_follow_import.append('pyglet.libs.win32')
            compiler.no_follow_import.append('pyglet.libs.x11')
            compiler.no_follow_import.append('pyglet.window.win32')
            compiler.no_follow_import.append('pyglet.window.xlib')
            compiler.no_follow_import.append('pyglet.window.headless')
        elif platform.system() == "Linux":
            compiler.no_follow_import.append('pyglet.libs.win32')
            compiler.no_follow_import.append('pyglet.libs.darwin')
            compiler.no_follow_import.append('pyglet.window.win32')
            compiler.no_follow_import.append('pyglet.window.cocoa')
            compiler.no_follow_import.append('pyglet.window.headless')

    print(compiler.output_path)

    print(compiler)

    print(compiler.gen_subprocess_cmd())

    # 确认是否需要编译
    # 如果包含 -y 参数 则直接编译
    if (('-y' or '-n') not in sys.argv) and (not is_github):
        while (do_compile := input('Do you want to compile this file? (y/n) ')) not in ['y', 'n']:
            pass
    elif '-y' in sys.argv:
        do_compile = 'y'
    elif is_github:
        do_compile = 'y'
    else:
        do_compile = 'n'

    if do_compile == 'y':
        # 编译
        time.sleep(1)  # 等待 1s
        start_time = time.time_ns()
        subprocess.run(compiler.gen_subprocess_cmd())
        print('Compile Done!')
        print(f'Compile Time: {time.time_ns() - start_time} ns ({(time.time_ns() - start_time) / 1000_000_000} s)')
        if is_github:
            # 去除无用字体文件
            try:
                shutil.rmtree(compiler.output_path / 'DR.dist/libs/fonts' / 'Fira_Code', ignore_errors=True)
                shutil.rmtree(compiler.output_path / 'DR.dist/libs/fonts' / 'scientifica', ignore_errors=True)
                shutil.rmtree(compiler.output_path / 'DR.dist/libs/fonts' / 'HarmonyOS_Sans' / 'HarmonyOS_Sans_Condensed', ignore_errors=True)
                shutil.rmtree(compiler.output_path / 'DR.dist/libs/fonts' / 'HarmonyOS_Sans' / 'HarmonyOS_Sans', ignore_errors=True)
                os.remove(compiler.output_path / 'DR.dist/libs/fonts' / 'Monocraft.otf')
                os.remove(compiler.output_path / 'DR.dist/libs/fonts' / 'SmileySans-Oblique.ttf')
            except Exception:
                traceback.print_exc()
            print('Remove Useless Files Done!')
            # 压缩
            with zipfile.ZipFile(Path('./build/Difficult_Rocket.zip'), 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as dist_zip:
                for path, sub_paths, sub_files in os.walk(compiler.output_path / 'DR.dist'):
                    print(f'writing {path}')
                    for file in sub_files:
                        file_path = os.path.join(path, file)
                        dist_zip.write(file_path)
            print('Zip Done!')
        elif platform.system() == 'Windows':
            dist_dir_size = 0
            for path, sub_paths, sub_files in os.walk(compiler.output_path / 'DR.dist'):
                for file in sub_files:
                    file_path = os.path.join(path, file)
                    dist_dir_size += os.path.getsize(file_path)
            exec_size = os.path.getsize(compiler.output_path / 'DR.dist' / 'DR.exe')
            compile_data = {'compile_time_ns': time.time_ns() - start_time,
                            'compile_time_s': (time.time_ns() - start_time) / 1000_000_000,
                            'dist_size': dist_dir_size,
                            'dist_size_mb': dist_dir_size / 1024 / 1024,
                            'exec_size': exec_size,
                            'exec_size_mb': exec_size / 1024 / 1024}
            with open(compiler.output_path / f'../compile_data-{time.time()}.toml', 'w') as compile_data_file:
                tomlkit.dump(compile_data, compile_data_file)


    sys.exit(0)
