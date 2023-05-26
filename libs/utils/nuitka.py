#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

# 用于使用 nuitka 构建 DR
import platform
import traceback
from pathlib import Path
from typing import List

from Difficult_Rocket.api.types import Options
from libs.MCDR.version import Version


class Status(Options):
    name = 'Nuitka Build Status'

    output_path: Path = Path("./build/nuitka")
    src_file: Path = Path('DR.py')

    # 以下为 nuitka 的参数
    use_lto: bool = False
    use_clang: bool = True
    use_msvc: bool = True
    standalone: bool = True
    company_name: str = 'tool-shenjack-workshop'
    product_name: str = 'Difficult-Rocket'
    product_version: Version
    file_version: Version
    icon_path: Path = Path('textures/icon.png')

    def init(self, **kwargs) -> None:
        # 非 windows 平台不使用 msvc
        if platform.system() != 'Windows':
            self.use_msvc = False

    def load_file(self) -> bool:
        try:
            from Difficult_Rocket import DR_runtime
            self.product_version = DR_runtime.DR_version
            self.file_version = DR_runtime.Build_version
            return True
        except ImportError:
            traceback.print_exc()
            return False

    def gen_subprocess_cmd(self) -> List[str]:
        cmd_list = ['python', '-m', 'nuitka']
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


        cmd_list += icon_cmd
        return cmd_list


