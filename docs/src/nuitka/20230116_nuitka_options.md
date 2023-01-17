# nuitka 1.3.7 编译选项说明

## [nuitka 所有编译选项原文](nuitka_options_137.md)

## 用法:
`__main__.py [--module] [--run] [options] main_module.py`

## 主要选项:
- `--help` 
  - 展示这条信息，然后退出

- `--version` 
  - 展示版本信息和用于汇报 bug 的重要细节，然后退出
  - 默认: `禁用`

- `--module`              
  - 创建一个扩展而不是可执行程序
  - 默认: `禁用`

- `--standalone`          
  - 启用独立环境模式输出
  - 可以允许你将输出的内容直接复制到其他系统相同的电脑上并且不用安装 Python 环境
  - 这也会意味着输出文件会变大
  - 在启用此选项是同样意味着启用
    - `--follow-imports`
    - `--python-flag=no_site`
  - 默认: `禁用`

- `--onefile`             
  - 基于独立环境模式的同时将输出内容变为单个可执行文件
  - 默认: `禁用`

- `--python-debug`
  - 是否使用 debug 版本
  - 默认: 运行 nuitka 的 Python 版本

- `--python-flag=FLAG`
  - Python 运行标志
  - 这个标志会强制改变运行标志
  - 目前受支持的选项
    - `-S`: `no_site` 的缩写
    - `static_hashes`: 禁用随机哈希
    - `no_warnings`: 不输出 Python 的运行时警告
    - `-O`: `no_asserts` 的缩写
    - `no_docstrings`: 不在编译中包含注释
    - `-u`: `unbuffered` 的缩写
    - `-m`: 运行模块
  - 默认: 运行 nuitka 的 Python 运行标志

- `--python-for-scons=PATH`
  - 如果正在用 Python 3.3/3.4 将自动生成一个可以让 Scons 使用的 Python 二进制库

    否则 nuitka 将使用运行 nuitka 的 Python 目录或者 Windows 注册表中的 Python 安装路径

    在 Python 3.5+ 是需要的? 在 非 Windows 上 Python 2.6/2.7 也需要

## 编译模块和内容选项:

  - `--include-package=PACKAGE`
    - 编译给定的整个模块和子包
    - 输入格式: Python 命名空间
      - 例如: `一个模块.的子包`
    - nuitka 会寻找并编译这个包和他的所有子包，并且让给定的包可以在代码中引用
    - 默认: 空

  - `--include-module=MODULE`
    - 编译给定的单个模块
    - 输入格式: Python 命名空间
      - 例如: `一个模块.的子包`
    - nuitka 会寻找并编译这个模块，并让给定的包可以在代码中引用

  - `--include-plugin-directory=MODULE/PACKAGE`
                          Include also the code found in that directory,
                          considering as if they are each given as a main file.
                          Overrides all other inclusion options. You ought to
                          prefer other inclusion options, that go by names,
                          rather than filenames, those find things through being
                          in "sys.path". This option is for very special use
                          cases only. Can be given multiple times. Default
                          empty.

  - `--include-plugin-files=PATTERN`
                          Include into files matching the PATTERN. Overrides all
                          other follow options. Can be given multiple times.
                          Default empty.

  - `--prefer-source-code`
                          For already compiled extension modules, where there is
                          both a source file and an extension module, normally
                          the extension module is used, but it should be better
                          to compile the module from available source code for
                          best performance. If not desired, there is --no-
                          prefer-source-code to disable warnings about it.
                          Default off.

    Control the following into imported modules:

  - `--follow-imports    Descend into all imported modules. Defaults to on in`
                          standalone mode, otherwise off.

  - `--follow-import-to=MODULE/PACKAGE`
                          Follow to that module if used, or if a package, to the
                          whole package. Can be given multiple times. Default
                          empty.

  - `--nofollow-import-to=MODULE/PACKAGE`
                          Do not follow to that module name even if used, or if
                          a package name, to the whole package in any case,
                          overrides all other options. Can be given multiple
                          times. Default empty.

  - `--nofollow-imports  Do not descend into any imported modules at all,`
                          overrides all other inclusion options and not usable
                          for standalone mode. Defaults to off.

  - `--follow-stdlib     Also descend into imported modules from standard`
                          library. This will increase the compilation time by a
                          lot and is also not well tested at this time and
                          sometimes won't work. Defaults to off.

### Onefile 选项:

  - `--onefile-tempdir-spec=ONEFILE_TEMPDIR_SPEC`
                          Use this as a folder to unpack to in onefile mode.
                          Defaults to '%TEMP%/onefile_%PID%_%TIME%', i.e. user
                          temporary directory and being non-static it's removed.
                          Use e.g. a string like
                          '%CACHE_DIR%/%COMPANY%/%PRODUCT%/%VERSION%' which is a
                          good static cache path, this will then not be removed.

### 数据文件:

  - `--include-package-data=PACKAGE`
                          Include data files for the given package name. DLLs
                          and extension modules are not data files and never
                          included like this. Can use patterns the filenames as
                          indicated below. Data files of packages are not
                          included by default, but package configuration can do
                          it. This will only include non-DLL, non-extension
                          modules, i.e. actual data files. After a ":"
                          optionally a filename pattern can be given as well,
                          selecting only matching files. Examples: "--include-
                          package-data=package_name" (all files) "--include-
                          package-data=package_name=*.txt" (only certain type) "
                      -
  - `--include-package-data=package_name=some_filename.dat`
    - (concrete file) Default empty.

  - `--include-data-files=DESC`
                          Include data files by filenames in the distribution.
                          There are many allowed forms. With '--include-data-
                          files=/path/to/file/*.txt=folder_name/some.txt' it
                          will copy a single file and complain if it's multiple.
                          With '--include-data-
                          files=/path/to/files/*.txt=folder_name/' it will put
                          all matching files into that folder. For recursive
                          copy there is a form with 3 values that '--include-
                          data-files=/path/to/scan=folder_name=**/*.txt' that
                          will preserve directory structure. Default empty.

  - `--include-data-dir=DIRECTORY`
                          Include data files from complete directory in the
                          distribution. This is recursive. Check '--include-
                          data-files' with patterns if you want non-recursive
                          inclusion. An example would be '--include-data-
                          dir=/path/some_dir=data/some_dir' for plain copy, of
                          the whole directory. All files are copied, if you want
                          to exclude files you need to remove them beforehand,
                          or use '--noinclude-data-files' option to remove them.
                          Default empty.

  - `--noinclude-data-files=PATTERN`
                          Do not include data files matching the filename
                          pattern given. This is against the target filename,
                          not source paths. So to ignore a file pattern from
                          package data for "package_name" should be matched as
                          "package_name/*.txt". Or for the whole directory
                          simply use "package_name". Default empty.

### DLL 文件:

  - `--noinclude-dlls=PATTERN`
                          Do not include DLL files matching the filename pattern
                          given. This is against the target filename, not source
                          paths. So ignore a DLL "someDLL" contained in the
                          package "package_name" it should be matched as
                          "package_name/someDLL.*". Default empty.

  - `--list-package-dlls=LIST_PACKAGE_DLLS`
                          Output the DLLs found for a given package name.
                          Default not done.

### 哪些警告会给到 Nuitka:

  - `--warn-implicit-exceptions`
                          Enable warnings for implicit exceptions detected at
                          compile time.

  - `--warn-unusual-code`
                          Enable warnings for unusual code detected at compile
                          time.

  - `--assume-yes-for-downloads`
                          Allow Nuitka to download external code if necessary,
                          e.g. dependency walker, ccache, and even gcc on
                          Windows. To disable, redirect input from nul device,
                          e.g. "</dev/null" or "<NUL:". Default is to prompt.

  - `--nowarn-mnemonic=MNEMONIC`
                          Disable warning for a given mnemonic. These are given
                          to make sure you are aware of certain topics, and
                          typically point to the Nuitka website. The mnemonic is
                          the part of the URL at the end, without the HTML
                          suffix. Can be given multiple times and accepts shell
                          pattern. Default empty.

    Immediate execution after compilation:

  - `--run`
    - 编译后立即运行二进制文件(或者导入编译的模块)
    - 默认: `禁用`

  - `--debugger`
    - 在 debugger 中运行
      - 例如: "gdb" 或 "lldb"
    - 用于自动获取堆栈跟踪
    - 默认: `禁用`

  - `--execute-with-pythonpath`
                          When immediately executing the created binary or
                          module using '--run', don't reset 'PYTHONPATH'
                          environment. When all modules are successfully
                          included, you ought to not need PYTHONPATH anymore,
                          and definitely not for standalone mode.

    Compilation choices:

  - `--user-package-configuration-file=YAML_FILENAME`
                          User provided Yaml file with package configuration.
                          You can include DLLs, remove bloat, add hidden
                          dependencies. Check User Manual for a complete
                          description of the format to use. Can be given
                          multiple times. Defaults to empty.

  - `--full-compat       Enforce absolute compatibility with CPython. Do not`
                          even allow minor deviations from CPython behavior,
                          e.g. not having better tracebacks or exception
                          messages which are not really incompatible, but only
                          different or worse. This is intended for tests only
                          and should *not* be used.

  - `--file-reference-choice=MODE`
                          Select what value "__file__" is going to be. With
                          "runtime" (default for standalone binary mode and
                          module mode), the created binaries and modules, use
                          the location of themselves to deduct the value of
                          "__file__". Included packages pretend to be in
                          directories below that location. This allows you to
                          include data files in deployments. If you merely seek
                          acceleration, it's better for you to use the
                          "original" value, where the source files location will
                          be used. With "frozen" a notation "<frozen
                          module_name>" is used. For compatibility reasons, the
                          "__file__" value will always have ".py" suffix
                          independent of what it really is.

  - `--module-name-choice=MODE`
                          Select what value "__name__" and "__package__" are
                          going to be. With "runtime" (default for module mode),
                          the created module uses the parent package to deduce
                          the value of "__package__", to be fully compatible.
                          The value "original" (default for other modes) allows
                          for more static optimization to happen, but is
                          incompatible for modules that normally can be loaded
                          into any package.

    Output choices:

  - `--output-filename=FILENAME`
                          Specify how the executable should be named. For
                          extension modules there is no choice, also not for
                          standalone mode and using it will be an error. This
                          may include path information that needs to exist
                          though. Defaults to '<program_name>' on this platform.
                          .exe

  - `--output-dir=DIRECTORY`
                          Specify where intermediate and final output files
                          should be put. The DIRECTORY will be populated with
                          build folder, dist folder, binaries, etc. Defaults to
                          current directory.

  - `--remove-output     Removes the build directory after producing the module`
                          or exe file. Defaults to off.

  - `--no-pyi-file       Do not create a ".pyi" file for extension modules`
                          created by Nuitka. This is used to detect implicit
                          imports. Defaults to off.

## Debug 特性:

  - `--debug             Executing all self checks possible to find errors in`
                          Nuitka, do not use for production. Defaults to off.

  - `--unstripped        Keep debug info in the resulting object file for`
                          better debugger interaction. Defaults to off.

  - `--profile`
    - 启用基于 `vmprof` 的效率检测
    - 现在还用不了
    - 默认: `禁用`

  - `--internal-graph    Create graph of optimization process internals, do not`
                          use for whole programs, but only for small test cases.
                          Defaults to off.

  - `--trace-execution   Traced execution output, output the line of code`
                          before executing it. Defaults to off.

  - `--recompile-c-only  This is not incremental compilation, but for Nuitka`
                          development only. Takes existing files and simply
                          compile them as C again. Allows compiling edited C
                          files for quick debugging changes to the generated
                          source, e.g. to see if code is passed by, values
                          output, etc, Defaults to off. Depends on compiling
                          Python source to determine which files it should look
                          at.

  - `--xml=XML_FILENAME  Write the internal program structure, result of`
                          optimization in XML form to given filename.

  - `--generate-c-only`
    - 仅编译成 C 代码，不编译为可执行文件或者模块
    - 此选项是为了那些不想浪费 CPU 资源的 单纯为了 debug 或者 覆盖率检测的编译
      - 不要觉得你能直接做到这样
    - 默认: `禁用`

  - `--experimental=FLAG`
                          Use features declared as 'experimental'. May have no
                          effect if no experimental features are present in the
                          code. Uses secret tags (check source) per experimented
                          feature.

  - `--low-memory        Attempt to use less memory, by forking less C`
                          compilation jobs and using options that use less
                          memory. For use on embedded machines. Use this in case
                          of out of memory problems. Defaults to off.

### 后端 C 编译器选项:

  - `--clang
    - 强制使用 `clang` 编译器
    - 在 Windows 上需要一个可用的 Visual Studio Enforce the use of clang. On Windows this requires a`
                            working Visual Studio version to piggy back on.
                            Defaults to off.

  - `--mingw64
    - 在 Windows 上强制使用 MinGW64 编译器
      - 除非运行在 MSYS2 和 Mingw 编译的 Python 上
    - 默认: `禁用`

  - `--msvc=MSVC_VERSION`
    - 在 Windows 上强制使用给定版本的 MSVC 编译器
                            Enforce the use of specific MSVC version on Windows.
                            Allowed values are e.g. "14.3" (MSVC 2022) and other
                            MSVC version numbers, specify "list" for a list of
                            installed compilers, or use "latest".  Defaults to
                            latest MSVC being used if installed, otherwise MinGW64
                            is used.

  - `--jobs=N
    - 指定最多可同时运行的 C 编译器数量
    - 默认: 你的 CPU 线程数

  - `--lto=choice
    - 使用 来自编译器的 链接时间优化
    - Use link time optimizations (MSVC, gcc, clang).`
                            Allowed values are "yes", "no", and "auto" (when it's
                            known to work). Defaults to "auto".

  - `--static-libpython=choice`
                          Use static link library of Python. Allowed values are
                          "yes", "no", and "auto" (when it's known to work).
                          Defaults to "auto".

    Cache Control:

  - `--disable-cache=DISABLED_CACHES`
                          Disable selected caches, specify "all" for all cached.
                          Currently allowed values are:
                          "all","ccache","bytecode","dll-dependencies". can be
                          given multiple times or with comma separated values.
                          Default none.

  - `--clean-cache=CLEAN_CACHES`
                          Clean the given caches before executing, specify "all"
                          for all cached. Currently allowed values are:
                          "all","ccache","bytecode","dll-dependencies". can be
                          given multiple times or with comma separated values.
                          Default none.

  - `--disable-bytecode-cache`
                          Do not reuse dependency analysis results for modules,
                          esp. from standard library, that are included as
                          bytecode. Same as --disable-cache=bytecode.

  - `--disable-ccache    Do not attempt to use ccache (gcc, clang, etc.) or`
                          clcache (MSVC, clangcl). Same as --disable-
                          cache=ccache.

  - `--disable-dll-dependency-cache`
                          Disable the dependency walker cache. Will result in
                          much longer times to create the distribution folder,
                          but might be used in case the cache is suspect to
                          cause errors. Same as --disable-cache=dll-
                          dependencies.

  - `--force-dll-dependency-cache-update`
                          For an update of the dependency walker cache. Will
                          result in much longer times to create the distribution
                          folder, but might be used in case the cache is suspect
                          to cause errors or known to need an update.

## PGO 编译选项:

  - `--pgo               Enables C level profile guided optimization (PGO), by`
                          executing a dedicated build first for a profiling run,
                          and then using the result to feedback into the C
                          compilation. Note: This is experimental and not
                          working with standalone modes of Nuitka yet. Defaults
                          to off.

  - `--pgo-args=PGO_ARGS`
                          Arguments to be passed in case of profile guided
                          optimization. These are passed to the special built
                          executable during the PGO profiling run. Default
                          empty.

  - `--pgo-executable=PGO_EXECUTABLE`
                          Command to execute when collecting profile
                          information. Use this only, if you need to launch it
                          through a script that prepares it to run. Default use
                          created program.

### Tracing features:

  - `--report=REPORT_FILENAME`
                          Report module, data files, compilation, plugin, etc.
                          details in an XML output file. This is also super
                          useful for issue reporting. Default is off.

  - `--quiet             Disable all information outputs, but show warnings.`
                          Defaults to off.

  - `--show-scons        Run the C building backend Scons with verbose`
                          information, showing the executed commands, detected
                          compilers. Defaults to off.

  - `--no-progressbar    Disable progress bars. Defaults to off.`

  - `--show-progress     Obsolete: Provide progress information and statistics.`
                          Disables normal progress bar. Defaults to off.

  - `--show-memory       Provide memory information and statistics. Defaults to`
                          off.

  - `--show-modules      Provide information for included modules and DLLs`
                          Obsolete: You should use '--report' file instead.
                          Defaults to off.

  - `--show-modules-output=PATH`
                          Where to output '--show-modules', should be a
                          filename. Default is standard output.

  - `--verbose           Output details of actions taken, esp. in`
                          optimizations. Can become a lot. Defaults to off.

  - `--verbose-output=PATH`
                          Where to output from '--verbose', should be a
                          filename. Default is standard output.

    General OS controls:

  - `--disable-console   When compiling for Windows or macOS, disable the`
                          console window and create a GUI application. Defaults
                          to off.

  - `--enable-console    When compiling for Windows or macOS, enable the`
                          console window and create a console application. This
                          disables hints from certain modules, e.g. "PySide"
                          that suggest to disable it. Defaults to true.

  - `--force-stdout-spec=FORCE_STDOUT_SPEC`
                          Force standard output of the program to go to this
                          location. Useful for programs with disabled console
                          and programs using the Windows Services Plugin of
                          Nuitka commercial. Defaults to not active, use e.g.
                          '%PROGRAM%.out.txt', i.e. file near your program.

  - `--force-stderr-spec=FORCE_STDERR_SPEC`
                          Force standard error of the program to go to this
                          location. Useful for programs with disabled console
                          and programs using the Windows Services Plugin of
                          Nuitka commercial. Defaults to not active, use e.g.
                          '%PROGRAM%.err.txt', i.e. file near your program.

    Windows specific controls:

  - `--windows-icon-from-ico=ICON_PATH`
                          Add executable icon. Can be given multiple times for
                          different resolutions or files with multiple icons
                          inside. In the later case, you may also suffix with
                          #<n> where n is an integer index starting from 1,
                          specifying a specific icon to be included, and all
                          others to be ignored.

  - `--windows-icon-from-exe=ICON_EXE_PATH`
                          Copy executable icons from this existing executable
                          (Windows only).

  - `--onefile-windows-splash-screen-image=SPLASH_SCREEN_IMAGE`
                          When compiling for Windows and onefile, show this
                          while loading the application. Defaults to off.

  - `--windows-uac-admin`
                          Request Windows User Control, to grant admin rights on
                          execution. (Windows only). Defaults to off.

  - `--windows-uac-uiaccess`
                          Request Windows User Control, to enforce running from
                          a few folders only, remote desktop access. (Windows
                          only). Defaults to off.

    macOS specific controls:

  - `--macos-target-arch=MACOS_TARGET_ARCH`
                          What architectures is this to supposed to run on.
                          Default and limit is what the running Python allows
                          for. Default is "native" which is the architecture the
                          Python is run with.

  - `--macos-create-app-bundle`
                          When compiling for macOS, create a bundle rather than
                          a plain binary application. Currently experimental and
                          incomplete. Currently this is the only way to unlock
                          disabling of console.Defaults to off.

  - `--macos-app-icon=ICON_PATH`
                          Add icon for the application bundle to use. Can be
                          given only one time. Defaults to Python icon if
                          available.

  - `--macos-signed-app-name=MACOS_SIGNED_APP_NAME`
                          Name of the application to use for macOS signing.
                          Follow "com.YourCompany.AppName" naming results for
                          best results, as these have to be globally unique, and
                          will potentially grant protected API accesses.

  - `--macos-app-name=MACOS_APP_NAME`
                          Name of the product to use in macOS bundle
                          information. Defaults to base filename of the binary.

  - `--macos-app-mode=MODE`
                          Mode of application for the application bundle. When
                          launching a Window, and appearing in Docker is
                          desired, default value "gui" is a good fit. Without a
                          Window ever, the application is a "background"
                          application. For UI elements that get to display
                          later, "ui-element" is in-between. The application
                          will not appear in dock, but get full access to
                          desktop when it does open a Window later.

  - `--macos-sign-identity=MACOS_APP_VERSION`
                          When signing on macOS, by default an ad-hoc identify
                          will be used, but with this option your get to specify
                          another identity to use. The signing of code is now
                          mandatory on macOS and cannot be disabled. Default
                          "ad-hoc" if not given.

  - `--macos-sign-notarization`
                          When signing for notarization, using a proper TeamID
                          identity from Apple, use the required runtime signing
                          option, such that it can be accepted.

  - `--macos-app-version=MACOS_APP_VERSION`
                          Product version to use in macOS bundle information.
                          Defaults to "1.0" if not given.

  - `--macos-app-protected-resource=RESOURCE_DESC`
                          Request an entitlement for access to a macOS protected
                          resources, e.g.
                          "NSMicrophoneUsageDescription:Microphone access for
                          recording audio." requests access to the microphone
                          and provides an informative text for the user, why
                          that is needed. Before the colon, is an OS identifier
                          for an access right, then the informative text. Legal
                          values can be found on https://developer.apple.com/doc
                          umentation/bundleresources/information_property_list/p
                          rotected_resources and the option can be specified
                          multiple times. Default empty.

    Linux specific controls:

  - `--linux-icon=ICON_PATH`
                          Add executable icon for onefile binary to use. Can be
                          given only one time. Defaults to Python icon if
                          available.

    Binary Version Information:

  - `--company-name=COMPANY_NAME`
                          Name of the company to use in version information.
                          Defaults to unused.

  - `--product-name=PRODUCT_NAME`
                          Name of the product to use in version information.
                          Defaults to base filename of the binary.

  - `--file-version=FILE_VERSION`
                          File version to use in version information. Must be a
                          sequence of up to 4 numbers, e.g. 1.0 or 1.0.0.0, no
                          more digits are allowed, no strings are allowed.
                          Defaults to unused.

  - `--product-version=PRODUCT_VERSION`
                          Product version to use in version information. Same
                          rules as for file version. Defaults to unused.

  - `--file-description=FILE_DESCRIPTION`
                          Description of the file used in version information.
                          Windows only at this time. Defaults to binary
                          filename.

  - `--copyright=COPYRIGHT_TEXT`
                          Copyright used in version information. Windows only at
                          this time. Defaults to not present.

  - `--trademarks=TRADEMARK_TEXT`
                          Copyright used in version information. Windows only at
                          this time. Defaults to not present.

    Plugin control:

  - `--enable-plugin=PLUGIN_NAME`
                          Enabled plugins. Must be plug-in names. Use '--plugin-
                          list' to query the full list and exit. Default empty.

  - `--disable-plugin=PLUGIN_NAME`
                          Disabled plugins. Must be plug-in names. Use '--
                          plugin-list' to query the full list and exit. Most
                          standard plugins are not a good idea to disable.
                          Default empty.

  - `--plugin-no-detection`
                          Plugins can detect if they might be used, and the you
                          can disable the warning via "--disable-plugin=plugin-
                          that-warned", or you can use this option to disable
                          the mechanism entirely, which also speeds up
                          compilation slightly of course as this detection code
                          is run in vain once you are certain of which plugins
                          to use. Defaults to off.

  - `--plugin-list       Show list of all available plugins and exit. Defaults`
                          to off.

  - `--user-plugin=PATH  The file name of user plugin. Can be given multiple`
                          times. Default empty.

  - `--show-source-changes`
                          Show source changes to original Python file content
                          before compilation. Mostly intended for developing
                          plugins. Default False.

    Plugin options of 'anti-bloat':

  - `--show-anti-bloat-changes`
                          Annotate what changes are by the plugin done.

  - `--noinclude-setuptools-mode=NOINCLUDE_SETUPTOOLS_MODE`
                          What to do if a 'setuptools' or import is encountered.
                          This package can be big with dependencies, and should
                          definitely be avoided. Also handles 'setuptools_scm'.

  - `--noinclude-pytest-mode=NOINCLUDE_PYTEST_MODE`
                          What to do if a 'pytest' import is encountered. This
                          package can be big with dependencies, and should
                          definitely be avoided. Also handles 'nose' imports.

  - `--noinclude-unittest-mode=NOINCLUDE_UNITTEST_MODE`
                          What to do if a unittest import is encountered. This
                          package can be big with dependencies, and should
                          definitely be avoided.

  - `--noinclude-IPython-mode=NOINCLUDE_IPYTHON_MODE`
                          What to do if a IPython import is encountered. This
                          package can be big with dependencies, and should
                          definitely be avoided.

  - `--noinclude-dask-mode=NOINCLUDE_DASK_MODE`
                          What to do if a 'dask' import is encountered. This
                          package can be big with dependencies, and should
                          definitely be avoided.

  - `--noinclude-numba-mode=NOINCLUDE_NUMBA_MODE`
                          What to do if a 'numba' import is encountered. This
                          package can be big with dependencies, and is currently
                          not working for standalone. This package is big with
                          dependencies, and should definitely be avoided.

  - `--noinclude-default-mode=NOINCLUDE_DEFAULT_MODE`
                          This actually provides the default "warning" value for
                          above options, and can be used to turn all of these
                          on.

  - `--noinclude-custom-mode=CUSTOM_CHOICES`
                          What to do if a specific import is encountered. Format
                          is module name, which can and should be a top level
                          package and then one choice, "error", "warning",
                          "nofollow", e.g. PyQt5:error.