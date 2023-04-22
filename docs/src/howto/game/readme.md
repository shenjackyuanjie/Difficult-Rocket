# Difficult Rocket 游戏功能设计文档

> by shenjackyuanjie and BlueFunny_

`Difficult Rocket` 游戏本体功能由 `DR mod` 实现

## DR mod

- `DR mod` 包含以下几个部分
  - `DR_mod`: Python 实现的主体
  - `DR_rs`: DR_mod 的 Rust 扩展

- 命名空间
  - 命名空间遵循本体原则 全拼
  - `Difficult_Rocket_mod`
  - `Difficult_Rocket_rs`

## DR_rs

> DR_rs 扩展为 DR mod 的 Rust 扩展

- 内容
  - `simluation`
    - 物理引擎交互
  - `sr1_data`
    - SR1 数据读取 格式转化
  - `types`
    - 主要的 Rust 数据格式定义

### `DR_rs` Rust 插件加载逻辑

- 加载模式
    - 冷加载
      - 游戏启动前扫描 Rust 扩展目录, 并加载所有的可识别后缀名扩展, 然后启动游戏
    - 热加载
      - 游戏进行中进行 `热加载` / `热卸载` / `热重载` 等操作
        - **不推荐使用此方式, 因为这可能导致某些插件未正常加载导致异常**
        - 使用此方式必须提供**明确的**初始化加载阶段, 否则将拒绝加载
          - PS: 这个初始化加载阶段指扩展应在何时加载, 如启动时, 这个具体是看扩展都要修改哪些内容的
- 加载方法
  - 利用 [本文](https://docs.rs/libloading/latest/libloading/) 中的方法加载 dll 扩展模组
    - 模组应明确提供以下信息 (加 `*` 为可选内容)
      - 模组名称
      - 模组唯一可识别 ID
      - 模组版本
      - 模组作者
      - 模组作者链接
      - *模组描述 (限制字数在 x 以内)
        - x 暂未确定
      - 模组兼容游戏版本 (carte 版本表达式)
      - 模组使用的 DR SDK 版本
        - 此处应由软件自动生成
      - 模组构建时的 DR SDK 版本
        - 此处应由软件自动生成
      - 模组使用的 DR SDK API 版本
      - 模组使用的 DR SDK 内部协议版本
      - *模组可选依赖 (包括版本)
      - 模组必选依赖

- DR SDK版本 和 DR API 版本都需要写，都需要最高和最低，
- 然后······ 版本号是四位的格式

- 调用手段
  - UI 调用
    - 模组添加
  - 软件内调用
    - 加载时调用
  - 我先睡了，老爹催了


