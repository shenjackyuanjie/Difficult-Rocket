# DR SDK 更新日志

- 最新版本号
  - DR sdk: 0.8.7.3
  - DR api: 0.1.1.0

## Draft DR sdk 0.9.0.0

### Rename

- `Api_version` -> `api_version`

### Add

- 添加内置依赖: `lib-not-dr`
  - Added built-in dependency: `lib-not-dr`
  - 不再同时维护两份代码
  - No longer maintain two sets of code at the same time

### Fix

- 如果没有 DR_game 的情况下, 退出时会 join 控制台线程
  - 通过检测线程是否是守护线程来判断是否 join
  - If there is no DR_game, join the console thread when exiting
    - Determine whether to join by detecting whether the thread is a daemon thread

### Dependency

- 更新了所有的依赖版本号
  - 去看 `requirements.txt` 吧
- Updated all dependency version numbers
  - Go see `requirements.txt`

## DR sdk 0.8.7.2

### Add

- `assets/fonts`
  - `unifont.otf`
    - `unifont v 15.1.02`

### Translate key

- Add
  - `client`
    - `load.font`
      - `start`
      - `file`
      - `error`
      - `use_time`

### Enhance

- `client.pyglet_load_fonts_folder`
  - 现在使用 `os.walk` 遍历文件夹
  - 使用 `tr` 进行日志记录

## DR sdk 0.8.7.1

### Add

- `BaseScreen`
  - 现在继承了 `Options`
  - 添加了 `name` 选项来识别名称
  - Now inherits `Options`
  - Added `name` option to identify name
- `gui.widget.PressTextButton`
  - 作为 gui 的一部分
  - 依然在测试阶段
  - 有人发现 bug 请务必发 issue, 十分感谢
  - As part of gui
  - Still in the testing phase
  - If you find a bug, please be sure to issue it, thank you very much

## DR sdk 0.8.7.0

### Add

- 添加了 `Difficult_Rocket.utils.camera.GroupCamera`
  - 和 `Difficult_Rocket.utils.camera.CenterGroupCamera`
  - 实际上就是使用 `pyglet.graphics.Group` 来实现的 `Camera`
  - 具有相同的功能
  - 顺便同样在 `api.camera` 里添加了导出
    - 这次我一定不会再忘记导出了
  - Added `Difficult_Rocket.utils.camera.GroupCamera`
  - And `Difficult_Rocket.utils.camera.CenterGroupCamera`
  - Actually, it is implemented `Camera` using `pyglet.graphics.Group`
  - Has the same function
  - By the way, the export was also added in `api.camera`
    - This time I will never forget to export it again
- 为所有 `xxCamera` 添加了
  - `reset` 方法
  - 用于一键重置缩放+平移
  - Added `reset` method for all `xxCamera`
    - Used to reset zoom + translation with one click

## DR sdk 0.8.6.1

### Fix

- 现在 `DR.py` 启动之后如果崩溃会在控制台输出完整的 Crash report 了
  - Now, after `DR.py` starts, if it crashes, the complete Crash report will be output to the console

## DR sdk 0.8.6.0

重构了一下项目结构

Refactored the project structure

### Fix

- issue [#42](https://github.com/shenjackyuanjie/Difficult-Rocket/issues/42)
  - Crash report 的时区不正确
    - Crash report time zone is incorrect

### Change

- 将大部分资源文件移动到 `assets/`
  - `libs/fonts` -> `assets/fonts`
  - `configs/lang` -> `assets/lang`
  - `configs/xxx.xml` -> `assets/builtin/xxx.xml`
  - `textures` -> `assets/textures`
  - Move all the resources to `assets/`

## DR sdk 0.8.5.2

### Fix

- `crash` 引用了已经重命名的 `Difficult_Rocket.game_version` (`Difficult_Rocket.sdk_version`)
- `Difficult_Rocket.api.types`
  - `VersionRequirement`
  - `VersionParsingError`

### Change

- 修改了 `DR.py`
  - 实际上是 `DR-start.py` 的改名
  - Changed `DR.py`
    - Actually renamed `DR-start.py`

### Clean

- 删除了 `DR-start.py`
  - 实际上是改成了 `DR.py`
  - Removed `DR-start.py`
    - Actually changed to `DR.py`
- 删除了 `libs/utils/dsm.py`
  - Deleted `libs/utils/dsm.py`

## DR sdk 0.8.5.1

### API

- 将 `Camera` 和 `CenterCamera` 添加到 `Difficult_Rocket.api.camera`
  - Add `Camera` and `CenterCamera` to `Difficult_Rocket.api.camera`

## DR sdk 0.8.5.0

### Changes

- `Difficult_Rocket.__init__`
  - 重命名 / Rename
  - `game_version` -> `sdk_version`
- `ModManager`
  - `get_mod_module(mod_name: str) -> Optional[ModInfo]`
    - 通过 mod 名称获取 mod 的信息
    - Get mod information by mod name
  - `load_mod(mod_path: Path) -> Optional[ModInfo]`
    - 加载指定路径的 mod
    - Load the mod at the specified path
  - `find_mods_in_path(extra_mods_path: Optional[List[Path]]) -> List[Path]`
    - 在指定的路径中查找 mod 并返回 mod 的路径
    - Find mods in the specified path and return the path of the mod
  - `unload_mod(mod_id: str, game: Game) -> Optional[ModInfo]`
    - 卸载指定的 mod 并返回 mod 的信息
    - Unload the specified mod and return the mod information
  - `reload_mod(mod_id: str, game: Game)`
    - 重新加载指定的 mod
    - Reload the specified mod

### Remove

- `DR.client.guis.widget.InputBox`
  - 没用了 `TextEntry` 已经好了 可以直接用了
  - Use Less, the `TextEntry` is ok to use

### Command

- `mods`
  - `list`
    - 列出所有已加载的 mod
    - List all loaded mods
  - `reload <mod_id>`
    - 重新加载指定的 mod
    - Reload the specified mod

## DR sdk 0.8.4.1

### Add

- `utils.camera`
  - `Camera`
    - 一个 2D 摄影机，可以用于高效变换渲染坐标
  - `CenterCamera`
    - 一个中心对器的 2D 摄影机，可以用于高效变换渲染坐标

## DR sdk 0.8.4.0

### Fix

- issue #33 (<https://github.com/shenjackyuanjie/Difficult-Rocket/issues/33>)
  - 修复了实际上并不会加载 `.otf` 格式的字体文件的问题

### language

- 去除了 `dr_game` 相关的键值
  - 现在这些键值已经在 `dr_game` 自己的语言文件中了
  - Removed the key values related to `dr_game`
    - Now these key values are in the language file of `dr_game` itself
- 将 mod 加载部分的键值独立出来
  - 这样调用起来更方便一些
  - Separate the key values of the mod loading part
    - This makes it easier to call

### 修改

- `utils.translate`
  - `Tr`
    - 现在支持自定义语言文件的路径了
      - `lang_path`
    - 用于给 mod 加载自己的语言文件
- 现在 `logging` 的配置转移到 `__init__` 中了
  - 保证调用 `logging` 的时候可以正常使用
  - Now the configuration of `logging` is moved to `__init__`
    - Ensure that `logging` can be used normally when called
- 现在输入命令之后不会输出一个 `True`/`False` 了
  - (实际上是用来检测命令是不是用 `/` 开头的)
  - Now, the command will not output a `True`/`False`
    - (Actually used to detect whether the command starts with `/`)
- `CommandText`
  - `find`
    - 现在会先用 `str.startswith` 检测是否以要求的字符串开头
      - 实际上就是丐版 `re.match`
    - 并且会在匹配上之后 如果匹配内容后面第一个字符是空格 则会截取掉空格
    - Now, it will first use `str.startswith` to detect whether it starts with the required string
      - Actually a poor version of `re.match`
    - And after matching, if the first character after the matching content is a space, the space will be intercepted

## DR sdk 0.8.3.0

### 删除

- `pyglet_rs`
  - 事实证明这玩意没啥用
  - Removed pyglet_rs

### Fix

- issue #31 (https://github.com/shenjackyuanjie/Difficult-Rocket/issues/31)
  - 窗口标题不正确 (实际上是因为只使用 `DR_runtime` 进行格式化)
  - Window title is incorrect

### 添加

- `DR_status`
  - 实际上就是 `DR_runtime`
  - `DR_runtime` -> `DR_status`
  - `client_running`
    - 客户端是否在运行
    - Is client running
  - `server_running`
    - 服务器是否在运行
    - Is server running
- Mod loader
  - 添加了对支持版本号的 warnings
  - Added warnings for supporting version numbers

### 移动

- `Difficult_Rocket.DR_runtime`
  - `DR_version` -> `DR_status.DR_version`
  - `API_version` -> `DR_status.API_version`
  - `Build_version` -> `DR_status.Build_version`
  - `default_language` -> `DR_status.default_language`

### 删除

- `Diffiuclt_Rocket.long_version`
  - 不再使用整数标记版本号 (反正 `Version` 有一个完整的版本号比较机制)
  - No longer use integer to mark version number (since `Version` has a complete version comparison mechanism)
- `Difficult_Rocket.DR_rust_available`
  - 似乎我忘记删掉这个 `DR_rs` 的耦合了

```python
long_version: int = 15
"""
long_version: 一个用于标记内部协议的整数
15: 完全移除 DR_rust 相关内容 解耦完成
14: BaseScreen 的每一个函数都添加了一个参数: window: "ClientWindow"
13: 为 DR_runtime 添加 API_version
12: 去除 DR_runtime 的 global_logger
    要 logging 自己拿去（
11: 为 DR_option  添加 use_DR_rust
    修复了一些拼写错误
10: 为 DR_runtime 添加 DR_Rust_get_version
9 : 为 DR_option  添加 pyglet_macosx_dev_test
8 : 为 DR_runtime 添加 DR_rust_version
    为 DR_option  添加 DR_rust_available
    以后就有 DR_rust 了
7 : 为 DR_option 添加 std_font_size
6 : 事实证明, 不如直接用int
5 : 添加 build_version 信息,用于标记编译文件版本,
    游戏版本改为四位数，终于有一个可以让我随便刷的版本号位数了
4 : 把 translate 的字体常量位置改了一下,顺便调换顺序
3 : 就是试试改一下，正好 compiler 要用
2 : 哦，对 longlong 好耶！
1 : 我可算想起来还有这回事了 v0.6.4
"""
```

## DR sdk 0.8.2.0

### Fix

- issue #27 (https://github.com/shenjackyuanjie/Difficult_Rocket/issues/27)
- ~~为什么每次发完release都要修issue啊 font文件夹不存在就会报错~~

## DR sdk 0.8.1.0

### 删除

- `api.types.SR1`
  - 移动到 `dr_game` 中

### 添加

- `api.types`
  - 添加 `Version` (`libs.MCDR.version.Version`)
- `Difficult_Rocket.api.types.Options`
  - `str_option`
    - 获取一个所有键、值都是 builtin 类型的字典
    - 可以用于写入文件
  - `__str__`
  - `__repr__`
    - 让 `Options` 可以被 `print` 打印

### 修复 Bug

- 自带的 `console` 类在 `get_command` 时 没有检查是否为空
