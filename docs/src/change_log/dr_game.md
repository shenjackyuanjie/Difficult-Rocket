
# DR game/DR rs 更新日志

- 最新版本号
  - DR game: 0.1.1.0
  - DR rs: 0.2.9.0

## DR game 0.1.1.0

### 添加

- `types.py`
  - 从 `DR.api.types.SR1` 中移动过来

### 新功能

- `console.py`
  - 基于 `PyConsole`
  - 用于替换 `DR sdk` 的默认控制台方法

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

