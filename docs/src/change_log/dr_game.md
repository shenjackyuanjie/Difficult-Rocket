
# DR game/DR rs 更新日志

- 最新版本号
  - DR game: 0.2.0.0
  - DR rs: 0.2.11.0

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

