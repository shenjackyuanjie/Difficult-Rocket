
# DR game/DR rs 更新日志

- 最新版本号
  - DR game: 0.2.1.0
  - DR rs: 0.2.15.0

## DR rs 0.3.0.0

### 修改

- 适配了 `DR sdk` 的关于 mods 的修改
  - Adapted the modification of mods about `DR sdk`
- `RustConsole`
  - 现在输入体验更好了
  - Now the input experience is better

## DR rs 0.2.15.0

### 修改

- 现在支持新的 mods reload 和 unload 了
  - 适配了 `DR sdk` 的关于 mods 的修改
  - Now support new mods reload and unload
    - Adapted the modification of mods about `DR sdk`

### 添加

- `IdType = i64`
  - 统一的 id 类型
  - Unified id type
- `PySR1Ship`
  - `get_connection -> Vec<(i32, i32, IdType, IdType)>`
    - 获取飞船的连接信息
    - Get the connection information of the ship

## DR rs 0.2.14.0

### 删除

- 删除了多个 xml 测试读取函数
  - Remove multiple xml test read functions

### 改进

- 改进了 xml writer 的 `SR1Ship` 写入
  - Improve the xml writer's `SR1Ship` write

## DR game 0.2.1.0

### 修改

- 将 `sr1_ship` 中的 `Camera_rs` 改为 `Difficult_Rocket.utils.camera.Camera`
  - Change `Camera_rs` in `sr1_ship` to `Difficult_Rocket.utils.camera.Camera`
- 添加了部件的连接线(都是彩色哒)
  - Add the connection line of the part (all are colored)

## DR rs 0.2.13.0

### 删除

- 删除了 `render.rs`
  - 没必要拿 rust 写这玩意（
  - 用 `DR game` 的 `camera` 代替
  - Delete `render.rs`
    - No need to write this thing with rust (
    - Use `DR game`'s `camera` instead

### 添加

- 添加了 基于 `quick-xml::writer::Writer` 的 xml `SR1Ship` 写入
  - 折磨啊啊啊啊啊啊啊啊
  - Add xml `SR1Ship` write based on `quick-xml::writer::Writer`
    - Torture ah ah ah ah ah ah ah ah

## DR rs 0.2.12.0

### 添加

- 添加了 xml 的读取测试
  - Add xml read test

## DR game 0.1.2.0

### 修改

- 现在渲染飞船的时候不会再显示那个白色框了
  - 改为一个彩色的框
- Now, the ship will not be displayed in the white box
  - Change to a colored box

## DR rs 0.2.11.0

### 添加

- `Python::data::PySR1Ship`
  - `get_part_box(&self, part_id: i64) -> Option<(f64, f64), (f64, f64)>`
    - 用于获取对应 id 的实际碰撞箱

## DR game 0.2.0.0

### 适配

- 适配了 `DR_sdk` `0.8.3.0` 的修改

## DR game 0.1.1.0

### 添加

- `types.py`
  - 从 `DR.api.types.SR1` 中移动过来

### 新功能

- `console.py`
  - 基于 `PyConsole`
  - 用于替换 `DR sdk` 的默认控制台方法

## DR rs 0.2.10.1

### `types.rs`

- 兼容了 `Option<Vec<Step>>` 的 `sr1_data.rs`
  - `Vec<Step>` -> `Option<Vec<Step>>`

### Bug 修复

- [#24](https://github.com/shenjackyuanjie/Difficult-Rocket/issues/24) `无法解析 带 staging 不带 steps的飞船`

## DR rs 0.2.10.0

### `python::PySR1PartType`

- 添加可从 Python 端获取的部件信息
  - `get_descriptiton -> String`
    - 部件描述 (Part description)
  - `get_sprite -> String`
    - 部件贴图 (Part sprite)
  - `get_width -> u32`
    - 部件宽度 (Part width)
  - `get_height -> u32`
    - 部件高度 (Part height)
  - `get_friction`
    - 部件摩擦系数 (Part friction)
  - `get_hidden`
    - 部件是否隐藏 (Part hidden)

## DR rs 0.2.9.3

### `sr1_data`

- `inflation`
  - `Option<bool>` -> `Option<f64>`

### Bug 修复

- [#21](https://github.com/shenjackyuanjie/Difficult-Rocket/issues/21) `field: "missing field Activate"`

## DR rs 0.2.9.2

### Bug 修复

- [#20](https://github.com/shenjackyuanjie/Difficult-Rocket/issues/20) `<DisconnectedParts/>`

## DR rs 0.2.9.1

### 实现

- `types::sr1::get_max_box`
  - 部分实现
- `types::math::Rotatable`
  - 添加了 mut 版方法

## DR rs 0.2.9.0

### 新功能

- `python::console::PyConsole`
  - 一个基于 `std::thread` 的多线程控制台
  - GIL 我谢谢你
  - 用于替换 `DR sdk` 的默认控制台方法
    - A multi-thread console based on `std::thread`
    - Used to replace the default console method of `DR sdk`

### Bug 修复

- [#19](https://github.com/shenjackyuanjie/Difficult-Rocket/issues/19) `BorrowMutError`

