
# DR SDK 更新日志

- 最新版本号
  - DR sdk: 0.8.2.0

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
- API
  - `Difficult_Rocket.api.log`
    - `get_named_client_logger`
    - `get_named_server_logger`
    - `get_named_main_logger`
      - 分别用于获取 基于 对应名称配置的 logger
      - Get the logger for the corresponding name configuration

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
