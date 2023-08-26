#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import platform
import warnings
from pathlib import Path
from typing import List, Tuple, Optional, Union, Any
from enum import Enum

from lib_not_dr.types import Options, Version, VersionRequirement


def ensure_cmd_readable(cmd: str) -> str:
    """
    保证 参数中 不含空格
    :param cmd: 要格式化的命令行参数
    :return: 格式化后的命令行参数
    """
    if ' ' in str(cmd):
        return f'"{cmd}"'
    return cmd


def format_cmd(arg_name: Optional[str] = None,
               arg_value: Optional[Union[str, List[str]]] = None,
               write: Optional[Any] = True) -> List[str]:
    """
    用来格式化输出命令行参数
    :param arg_name: 类似 --show-memory 之类的主项
    :param arg_value: 类似 xxx 类的内容
    :param write: 是否写入
    :return: 直接拼接好的命令行参数 不带 =
    """
    if not write:
        return []
    if arg_name is None:
        return []
    if arg_value is None:
        return [arg_name]
    if isinstance(arg_value, list):
        arg_value = ','.join([ensure_cmd_readable(value) for value in arg_value])
        return [f'{arg_name}{arg_value}']
    arg_value = ensure_cmd_readable(arg_value)
    return [f'{arg_name}{arg_value}']


class NuitkaSubConfig(Options):
    """
    Nuitka 配置的子项
    Nuitka configuration sub-items
    """
    name = 'Nuitka Sub Configuration'

    def gen_cmd(self) -> List[str]:
        """
        生成命令行参数
        :return:
        """
        raise NotImplementedError


class NuitkaPluginConfig(NuitkaSubConfig):
    """
    控制 nuitka 的 plugin 相关参数的部分
    Control part of nuitka's plugin related parameters
    """
    name = 'Nuitka Plugin Configuration'

    # --enable-plugin=PLUGIN_NAME
    enable_plugin: List[str] = []
    # --disable-plugin=PLUGIN_NAME
    disable_plugin: List[str] = []
    # --plugin-no-detection
    plugin_no_detection: bool = False
    # --user-plugin=PATH
    user_plugin: List[Path] = []
    # --show-source-changes
    show_source_changes: bool = False

    # --include-plugin-directory=MODULE/PACKAGE
    include_plugin_dir: List[str] = []
    # --include-plugin-files=PATTERN
    include_plugin_files: List[str] = []

    def gen_cmd(self) -> List[str]:
        lst = []
        lst += format_cmd('--enable-plugin=', self.enable_plugin, self.enable_plugin)
        lst += format_cmd('--disable-plugin=', self.disable_plugin, self.disable_plugin)
        lst += format_cmd('--plugin-no-detection' if self.plugin_no_detection else None)
        lst += format_cmd('--user-plugin=', [str(plugin.absolute()) for plugin in self.user_plugin], self.user_plugin)
        lst += format_cmd('--show-source-changes' if self.show_source_changes else None)
        lst += format_cmd('--include-plugin-directory=', self.include_plugin_dir, self.include_plugin_dir)
        lst += format_cmd('--include-plugin-files=', self.include_plugin_files, self.include_plugin_files)
        return lst


class NuitkaIncludeConfig(NuitkaSubConfig):
    """
    控制 nuitka 的 include 和 数据 相关参数的部分
    Control part of nuitka's include related parameters
    """
    name = 'Nuitka Include Configuration'

    # --include-package=PACKAGE
    include_packages: List[str] = []
    # --include-module=MODULE
    include_modules: List[str] = []

    # --prefer-source-code
    # --no-prefer-source-code    for --module
    prefer_source_code: bool = False
    # --follow-stdlib
    follow_stdlib: bool = False

    def gen_cmd(self) -> List[str]:
        lst = []
        lst += format_cmd('--include-package=', self.include_packages, self.include_packages)
        lst += format_cmd('--include-module=', self.include_modules, self.include_modules)
        lst += format_cmd('--prefer-source-code' if self.prefer_source_code else None)
        lst += format_cmd('--no-prefer-source-code' if not self.prefer_source_code else None)
        lst += format_cmd('--follow-stdlib' if self.follow_stdlib else None)
        return lst


class NuitkaDataConfig(NuitkaSubConfig):
    """
    控制 nuitka 的 数据 相关参数的部分
    Control part of nuitka's data related parameters
    """
    name = 'Nuitka Data Configuration'

    # --include-package-data=PACKAGE=PACKAGE_PATH
    include_package_data: List[Tuple[Path, Path]] = []
    # --include-data-files=PATH=PATH
    include_data_files: List[Tuple[Path, Path]] = []
    # --include-data-dir=DIRECTORY=PATH
    include_data_dir: List[Tuple[Path, Path]] = []

    # --noinclude-data-files=PATH
    no_include_data_files: List[Path] = []

    # --list-package-data=LIST_PACKAGE_DATA
    list_package_data: List[str] = []
    # --list-package-dlls=LIST_PACKAGE_DLLS
    list_package_dlls: List[str] = []

    # --include-distribution-metadata=DISTRIBUTION
    include_distribution_metadata: List[str] = []


class NuitkaBinaryInfo(Options):
    """
    nuitka 构建的二进制文件的信息
    nuitka build binary file information
    """
    name = 'Nuitka Binary Info'

    # --company-name=COMPANY_NAME
    company_name: Optional[str] = None
    # --product-name=PRODUCT_NAME
    product_name: Optional[str] = None

    # --file-version=FILE_VERSION
    # --macos-app-version=MACOS_APP_VERSION
    file_version: Optional[Union[str, Version]] = None
    # --product-version=PRODUCT_VERSION
    product_version: Optional[Union[str, Version]] = None

    # --file-description=FILE_DESCRIPTION
    file_description: Optional[str] = None
    # --copyright=COPYRIGHT_TEXT
    copyright: Optional[str] = None
    # --trademarks=TRADEMARK_TEXT
    trademarks: Optional[str] = None

    # Icon
    # --linux-icon=ICON_PATH
    # --macos-app-icon=ICON_PATH
    # --windows-icon-from-ico=ICON_PATH
    # --windows-icon-from-exe=ICON_EXE_PATH
    # 注意: 只有 Windows 下 才可以提供多个 ICO 文件
    # 其他平台 和 EXE 下只会使用第一个路径
    icon: Optional[List[Path]] = None

    # Console
    # --enable-console
    # --disable-console
    console: bool = True

    # Windows UAC
    # --windows-uac-admin
    windows_uac_admin: bool = False
    # --windows-uac-uiaccess
    windows_uac_ui_access: bool = False


class NuitkaOutputConfig(Options):
    """
    nuitka 构建的选项
    nuitka build output information
    """
    name = 'Nuitka Output Config'

    # --output-dir=DIRECTORY
    output_dir: Optional[Path] = None
    # --output-filename=FILENAME
    output_filename: Optional[str] = None

    # --quiet
    quiet: bool = False
    # --no-progressbar
    no_progressbar: bool = False
    # --verbose
    verbose: bool = False
    # --verbose-output=PATH
    verbose_output: Optional[Path] = None

    # --show-progress
    show_progress: bool = False
    # --show-memory
    show_memory: bool = False
    # --show-scons
    show_scons: bool = False
    # --show-modules
    show_modules: bool = False
    # --show-modules-output=PATH
    show_modules_output: Optional[Path] = None

    # --xml=XML_FILENAME
    xml: Optional[Path] = None
    # --report=REPORT_FILENAME
    report: Optional[Path] = None
    # --report-diffable
    report_diffable: bool = False

    # --remove-output
    remove_output: bool = False
    # --no-pyo-file
    no_pyo_file: bool = False


class NuitkaDebugConfig(Options):
    """
    nuitka 构建的调试选项
    nuikta build debug information
    """
    name = 'Nuitka Debug Config'

    # --debug
    debug: bool = False
    # --unstripped
    strip: bool = True
    # --profile
    profile: bool = False
    # --internal-graph
    internal_graph: bool = False
    # --trace-execution
    trace_execution: bool = False
    # --recompile-c-only
    recompile_c_only: bool = False
    # --generate-c-only
    generate_c_only: bool = False
    # --deployment
    deployment: bool = False
    # --no-deployment-flag=FLAG
    deployment_flag: Optional[str] = None
    # --experimental=FLAG
    experimental: Optional[str] = None


class NuitkaTarget(Enum):
    """
    用于指定 nuitka 构建的目标
    Use to specify the target of nuitka build
    exe: 不带任何参数
    module: --module
    standalone: --standalone
    one_file: --onefile
    """
    exe = ''
    module = 'module'
    standalone = 'standalone'
    one_file = 'package'


class NuitkaScriptGenerator(Options):
    """
    用于帮助生成 nuitka 构建脚本的类
    Use to help generate nuitka build script

    :arg main 需要编译的文件
    """
    name = 'Nuitka Script Generator'
    
    # --main=PATH
    # 可以有多个 输入时需要包在列表里
    main: List[Path]

    # --run
    run_after_build: bool = False
    # --debugger
    debugger: bool = False
    # --execute-with-pythonpath
    execute_with_python_path: bool = False

    # --assume-yes-for-downloads
    download_confirm: bool = True

    # standalone/one_file/module/exe
    target: NuitkaTarget = NuitkaTarget.exe

    # --python-debug
    python_debug: bool = False
    # --python-flag=FLAG
    python_flag: List[str] = []
    # --python-for-scons=PATH
    python_for_scons: Optional[Path] = None


class CompilerHelper(Options):
    """
    用于帮助生成 nuitka 构建脚本的类
    Use to help generate nuitka build script
    
    """
    name = 'Nuitka Compiler Helper'

    output_path: Path = Path('./build')
    src_file: Path

    python_cmd: str = 'python'
    compat_nuitka_version: VersionRequirement = VersionRequirement("~1.8.0")  # STATIC VERSION

    # 以下为 nuitka 的参数
    # nuitka options below
    use_lto: bool = False  # --lto=yes (no is faster)
    use_clang: bool = True  # --clang
    use_msvc: bool = True  # --msvc=latest
    use_mingw: bool = False  # --mingw64

    onefile: bool = False  # --onefile
    onefile_tempdir: Optional[str] = ''  # --onefile-tempdir-spec=
    standalone: bool = True  # --standalone
    use_ccache: bool = True  # not --disable-ccache
    enable_console: bool = True  # --enable-console / --disable-console

    show_progress: bool = True  # --show-progress
    show_memory: bool = False  # --show-memory
    remove_output: bool = True  # --remove-output
    save_xml: bool = False  # --xml
    xml_path: Path = Path('build/compile_data.xml')
    save_report: bool = False  # --report
    report_path: Path = Path('build/compile_report.xml')

    download_confirm: bool = True  # --assume-yes-for-download
    run_after_build: bool = False  # --run

    company_name: Optional[str] = ''
    product_name: Optional[str] = ''
    file_version: Optional[Version] = None
    product_version: Optional[Version] = None
    file_description: Optional[str] = ''  # --file-description

    copy_right: Optional[str] = ''  # --copyright

    icon_path: Optional[Path] = None

    follow_import: List[str] = []
    no_follow_import: List[str] = []

    include_data_dir: List[Tuple[str, str]] = []
    include_packages: List[str] = []

    enable_plugin: List[str] = []  # --enable-plugin=xxx,xxx
    disable_plugin: List[str] = []  # --disable-plugin=xxx,xxx

    def init(self, **kwargs) -> None:
        if (compat_version := kwargs.get('compat_nuitka_version')) is not None:
            if not self.compat_nuitka_version.accept(compat_version):
                warnings.warn(
                    f"Nuitka version may not compat with {compat_version}\n"
                    "requirement: {self.compat_nuitka_version}"
                )
        # 非 windows 平台不使用 msvc
        if platform.system() != 'Windows':
            self.use_msvc = False
            self.use_mingw = False
        else:
            self.use_mingw = self.use_mingw and not self.use_msvc
            # Windows 平台下使用 msvc 时不使用 mingw

    def __str__(self):
        return self.as_markdown()

    def as_markdown(self, longest: Optional[int] = None) -> str:
        """
        输出编译器帮助信息
        Output compiler help information
        
        Args:
            longest (Optional[int], optional): 
                输出信息的最大长度限制 The maximum length of output information. 
                Defaults to None.

        Returns:
            str: 以 markdown 格式输出的编译器帮助信息
                Compile helper information in markdown format
        """
        front = super().as_markdown(longest)
        gen_cmd = self.gen_subprocess_cmd()
        return f"{front}\n\n```bash\n{' '.join(gen_cmd)}\n```"

    def gen_subprocess_cmd(self) -> List[str]:
        """生成 nuitka 构建脚本
        Generate nuitka build script

        Returns:
            List[str]: 
                生成的 nuitka 构建脚本
                Generated nuitka build script
        """
        cmd_list = [self.python_cmd, '-m', 'nuitka']
        # macos 和 非 macos icon 参数不同
        if platform.system() == 'Darwin':
            cmd_list += format_cmd('--macos-app-version=', self.product_version, self.product_version)
            cmd_list += format_cmd('--macos-app-icon=', self.icon_path.absolute(), self.icon_path)
        elif platform.system() == 'Windows':
            cmd_list += format_cmd('--windows-icon-from-ico=', self.icon_path.absolute(), self.icon_path)
        elif platform.system() == 'Linux':
            cmd_list += format_cmd('--linux-icon=', self.icon_path.absolute(), self.icon_path)

        cmd_list += format_cmd('--lto=', 'yes' if self.use_lto else 'no')
        cmd_list += format_cmd('--clang' if self.use_clang else None)
        cmd_list += format_cmd('--msvc=latest' if self.use_msvc else None)
        cmd_list += format_cmd('--mingw64' if self.use_mingw else None)
        cmd_list += format_cmd('--standalone' if self.standalone else None)
        cmd_list += format_cmd('--onefile' if self.onefile else None)
        cmd_list += format_cmd('--onefile-tempdir-spec=', self.onefile_tempdir, self.onefile_tempdir)

        cmd_list += format_cmd('--disable-ccache' if not self.use_ccache else None)
        cmd_list += format_cmd('--show-progress' if self.show_progress else None)
        cmd_list += format_cmd('--show-memory' if self.show_memory else None)
        cmd_list += format_cmd('--remove-output' if self.remove_output else None)
        cmd_list += format_cmd('--assume-yes-for-download' if self.download_confirm else None)
        cmd_list += format_cmd('--run' if self.run_after_build else None)
        cmd_list += format_cmd('--enable-console' if self.enable_console else '--disable-console')

        cmd_list += format_cmd('--xml=', str(self.xml_path.absolute()), self.save_xml)
        cmd_list += format_cmd('--report=', str(self.report_path.absolute()), self.save_report)
        cmd_list += format_cmd('--output-dir=', str(self.output_path.absolute()), self.output_path)
        cmd_list += format_cmd('--company-name=', self.company_name, self.company_name)
        cmd_list += format_cmd('--product-name=', self.product_name, self.product_name)
        cmd_list += format_cmd('--file-version=', str(self.file_version), self.file_version)
        cmd_list += format_cmd('--product-version=', str(self.product_version), self.product_version)
        cmd_list += format_cmd('--file-description=', self.file_description, self.file_description)
        cmd_list += format_cmd('--copyright=', self.copy_right, self.copy_right)

        cmd_list += format_cmd('--follow-import-to=', self.follow_import, self.follow_import)
        cmd_list += format_cmd('--nofollow-import-to=', self.no_follow_import, self.no_follow_import)
        cmd_list += format_cmd('--enable-plugin=', self.enable_plugin, self.enable_plugin)
        cmd_list += format_cmd('--disable-plugin=', self.disable_plugin, self.disable_plugin)

        if self.include_data_dir:
            cmd_list += [f"--include-data-dir={src}={dst}" for src, dst in self.include_data_dir]
        if self.include_packages:
            cmd_list += [f"--include-package={package}" for package in self.include_packages]

        cmd_list.append(f"--main={self.src_file}")
        return cmd_list
