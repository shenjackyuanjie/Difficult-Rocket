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

from typing import Tuple, Dict
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

    # 检测 --no-pyglet-opt 参数
    pyglet_optimizations = True
    if pyglet_optimizations and '--no-pyglet-opt' not in sys.argv:

        compiler.no_follow_import += [f'pyglet.app.{x}' for x in ['win32', 'xlib', 'cocoa']]
        compiler.no_follow_import += [f'pyglet.input.{x}' for x in ['win32', 'linux', 'macos']]
        compiler.no_follow_import += [f'pyglet.libs.{x}' for x in ['win32', 'x11', 'wayland', 'darwin', 'egl', 'headless']]
        compiler.no_follow_import += [f'pyglet.window.{x}' for x in ['win32', 'xlib', 'cocoa', 'headless']]
        compiler.no_follow_import += [f'pyglet.canvas.{x}' for x in ['win32', 'xlib', 'xlib_vidmoderstore', 'cocoa', 'headless']]
        compiler.no_follow_import += [f'pyglet.gl.{x}' for x in ['win32', 'xlib', 'cocoa', 'headless']]

        mult_plat_libs = ['app', 'input', 'libs', 'window', 'canvas', 'gl']
        if platform.system() == "Windows":
            for lib in mult_plat_libs:
                compiler.no_follow_import.remove(f'pyglet.{lib}.win32')
        elif platform.system() == "Linux":
            for lib in mult_plat_libs:
                for name in ('xlib', 'x11', 'wayland', 'egl'):
                    if f'pyglet.{lib}.{name}' in compiler.no_follow_import:
                        compiler.no_follow_import.remove(f'pyglet.{lib}.{name}')
            compiler.no_follow_import.remove('pyglet.canvas.xlib_vidmoderstore')
        elif platform.system() == "Darwin":
            for lib in mult_plat_libs:
                for name in ('cocoa', 'darwin', 'macos'):
                    if f'pyglet.{lib}.{name}' in compiler.no_follow_import:
                        compiler.no_follow_import.remove(f'pyglet.{lib}.{name}')

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
            # 去除无用字体文件 (其实现在也不会打包字体文件了 因为 git lfs 没宽带了)
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
        else:
            dist_dir_size = 0
            dist_file_size: Dict[str, Tuple[int, float]] = {}
            for path, sub_paths, sub_files in os.walk(compiler.output_path / 'DR.dist'):
                for file in sub_files:
                    file_path = os.path.join(path, file)
                    dist_dir_size += os.path.getsize(file_path)
                    # 排除不需要记录的文件
                    if any(x in file_path for x in ('configs', 'libs', 'textures')):
                        continue
                    dist_file_size[file_path] = (os.path.getsize(file_path), os.path.getsize(file_path) / 1024 / 1024)
            compile_data = {'compile_time_ns': time.time_ns() - start_time,
                            'compile_time_s': (time.time_ns() - start_time) / 1000_000_000,
                            'dist_size': dist_dir_size,
                            'dist_size_mb': dist_dir_size / 1024 / 1024,
                            'compiler_data': compiler.str_option(),
                            'dist_file_size': dist_file_size}
            with open(compiler.output_path / f'../compile_data-{time.time()}.toml', 'w') as compile_data_file:
                tomlkit.dump(compile_data, compile_data_file)

    sys.exit(0)
