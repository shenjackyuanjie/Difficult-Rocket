#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

# 用于使用 nuitka 构建 DR
import platform
import traceback
from pathlib import Path
from typing import List, Tuple

from Difficult_Rocket.api.types import Options, Version


class Status(Options):
    name = 'Nuitka Build Status'

    output_path: Path = Path("./build/nuitka-win")
    src_file: Path = Path('DR.py')

    python_cmd: str = 'python'

    # 以下为 nuitka 的参数
    use_lto: bool = False  # --lto=yes (no is faster)
    use_clang: bool = True  # --clang
    use_msvc: bool = True  # --msvc=latest
    use_mingw: bool = False  # --mingw64
    standalone: bool = True  # --standalone
    use_ccache: bool = True  # not --disable-ccache

    show_progress: bool = True  # --show-progress
    show_memory: bool = False  # --show-memory

    download_confirm: bool = True  # --assume-yes-for-download

    company_name: str = 'tool-shenjack-workshop'
    product_name: str = 'Difficult-Rocket'
    product_version: Version
    file_version: Version

    icon_path: Path = Path('textures/icon.png')

    follow_import: List[str] = ['pyglet']
    no_follow_import: List[str] = ['objprint', 'pillow', 'PIL', 'cffi', 'pydoc', 'numpy']

    include_data_dir: List[Tuple[str, str]] = [('./libs/fonts', './libs/fonts'),
                                               ('./textures', './textures'),
                                               ('./configs', './configs')]
    include_packages: List[str] = ['Difficult_Rocket.api']

    def init(self, **kwargs) -> None:
        # 非 windows 平台不使用 msvc
        if platform.system() != 'Windows':
            self.use_msvc = False
            self.use_mingw = False
        else:
            self.use_mingw = self.use_mingw and not self.use_msvc
            # Windows 平台下使用 msvc 时不使用 mingw

    def load_file(self) -> bool:
        try:
            from Difficult_Rocket import DR_runtime
            self.product_version = DR_runtime.DR_version
            self.file_version = DR_runtime.Build_version
            return True
        except ImportError:
            traceback.print_exc()
            return False

    def __str__(self):
        return self.as_markdown()

    def as_markdown(self) -> str:
        front = super().as_markdown()
        gen_cmd = self.gen_subprocess_cmd()
        return f"{front}\n\n```bash\n{' '.join(gen_cmd)}\n```"

    def gen_subprocess_cmd(self) -> List[str]:
        cmd_list = [self.python_cmd, '-m', 'nuitka']
        # macos 和 非 macos icon 参数不同
        icon_cmd = ""
        if platform.system() == 'Darwin':
            icon_cmd = f"--macos-app-icon={self.icon_path.absolute()}"
        elif platform.system() == 'Windows':
            icon_cmd = f"--windows-icon-from-ico={self.icon_path.absolute()}"

        if self.use_lto:
            cmd_list.append('--lto=yes')
        else:
            cmd_list.append('--lto=no')

        if self.use_clang:
            cmd_list.append('--clang')
        if self.use_msvc:
            cmd_list.append('--msvc=latest')
        if self.standalone:
            cmd_list.append('--standalone')
        if not self.use_ccache:
            cmd_list.append('--disable-ccache')
        if self.show_progress:
            cmd_list.append('--show-progress')
        if self.show_memory:
            cmd_list.append('--show-memory')
        if self.download_confirm:
            cmd_list.append('--assume-yes-for-download')

        cmd_list.append(f"--output-dir={self.output_path.absolute()}")

        cmd_list.append(f"--company-name={self.company_name}")
        cmd_list.append(f"--product-name={self.product_name}")
        cmd_list.append(f"--product-version={self.product_version}")
        cmd_list.append(f"--file-version={self.file_version}")

        cmd_list.append(icon_cmd)

        cmd_list += [f"--include-data-dir={src}={dst}" for src, dst in self.include_data_dir]
        cmd_list += [f"--include-package={package}" for package in self.include_packages]

        cmd_list.append(f"--follow-import-to={','.join(self.follow_import)}")
        cmd_list.append(f"--nofollow-import-to={','.join(self.no_follow_import)}")

        cmd_list.append(f"{self.src_file}")
        return cmd_list
