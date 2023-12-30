# Difficult Rocket

中文 | [English](./docs/README-en.md)

- [GitHub](https://github.com/shenjackyuanjie/Difficult-Rocket)
- [Gitee](https://gitee.com/shenjackyuanjie/Difficult-Rocket)
- [Discord](https://discord.gg/kWzw2JrG6M)
- [Kook](https://kook.top/sRPjFG)

>注意：本仓库未来只会发布`DR SDK`的更新。`DR game`的更新会在[这里](https://github.com/shenjackyuanjie/DR-game)发布。

[![996.icu](https://img.shields.io/badge/996.icu-996.icu-red.svg)](https://996.icu)
[![semver](https://img.shields.io/badge/SemVer-2.0.0-blue.svg)](https://Semver.org/)
[![python-3.8.10](https://img.shields.io/badge/编写于_Python_版本-3.8.10-blue.svg)](https://Python.org)
[![pyglet-2.x](https://img.shields.io/badge/编写于_Pyglet_版本-2.x-blue.svg)](https://pyglet.org)
[![support python 3.8~12](https://img.shields.io/badge/Python-_3.8_~_3.12_-blue.svg)](https://Python.org)

## 版本

[关于版本号的说明](./docs/src/version.md)

[![release version](https://img.shields.io/badge/Release-0.8.7.2-blue.svg)](https://github.com/shenjackyuanjie/Difficult-Rocket/releases)
[![pre version](https://img.shields.io/badge/Pre_Release-0.8.7.2-blue.svg)](https://github.com/shenjackyuanjie/Difficult-Rocket/releases)
[![devlo version](https://img.shields.io/badge/Devloping-0.9.0-blue.svg)](https://github.com/shenjackyuanjie/Difficult-Rocket/releases)

[![language badge](https://stats.deeptrain.net/repo/shenjackyuanjie/Difficult-Rocket?theme=dark)](https://stats.deeptrain.net/repo/shenjackyuanjie/Difficult-Rocket?theme=dark)

[DR sdk 最新 Action 构建](https://nightly.link/shenjackyuanjie/Difficult-Rocket/workflows/nuitka/main)

[DR rs 最新 Action 构建](https://nightly.link/shenjackyuanjie/Difficult-Rocket/workflows/dr_rs/main)

## 介绍

这是一个用Python制作的类Simple Rocket游戏（简称：火箭模拟器）。相对于原版SR，它更加轻量。

[计划特性列表](docs/src/plan_features/README.md)

[YouTrack](https://difficult-rocket.youtrack.cloud/projects/8dafd498-59c0-4ce7-9900-d9292e9ed1f0)

[更新日志](docs/src/change_log/readme.md)

## 运行

### 1. Clone

```bash title="clone.sh"
mkdir DR
cd DR
git clone https://github.com/shenjackyuanjie/Difficult-Rocket.git
# 或者
git clone https://gitee.com/shenjackyuanjie/Difficult-Rocket.git
# 又或者
git clone git@github.com:shenjackyuanjie/Difficult-Rocket.git
```

### 2. 安装依赖

```bash title="install.sh"
python gen_require.py 0
python -m pip install -r requirements.txt
git submodule update --init --recursive
cd libs
python -m pip install ./lib_not_dr
python -m pip install ./pyglet
```

### 3. 运行

```bash title="run.sh"
python DR.py
```

## 环境需求

>开发环境使用的Python版本为`3.8.18`，但`3.8+`同样可用。

- `开发平台 1 - Windows 10 x64 22H2`
  - Python `3.8.10+`
    - `requirements`
  - `AMD R5 5600X`
  - `AMD RX 580 8G`

## 需要的Python模块

> python gen_require.py [-h] {0,1,2}
> run / build / compile

- `pyglet` (已经内置 V2.x 路径：`./libs/pyglet`)
- `xmltodict` (已经内置 V0.12.0 路径:`./libs/xmltodict`)
- `pyperclip` (已经内置 V1.8.2 路径: `./libs/pyperclip`)

## 鸣谢

- 开源项目
  - [pyglet](https://github.com/pyglet/pyglet) : GUI 和画面渲染
  - `tomlkit` : toml 解析器
  - `xmltodict`: xml 与 dict 转换器
  - `pyperclip`: 剪贴板!
  - [rapier2d](https://rapier.rs/) : 物理模拟引擎
  - [pyo3](https://pyo3.rs/main): Rust Python 扩展

- 主要贡献者
  - [@Rayawa](https://github.com/Rayawa) : 文档矫正 & 翻译部分 lang
  - [@rouxiao-you](https://github.com/ruoxiao-you) : 翻译 lang
  - [@Billchyi](https://github.com/Billchyi) : 文档矫正
  - [@MSDNicrosoft](https://github.com/MSDNicrosoft) : 优化代码

## 相关链接

[官方文档](https://dr.shenjack.top)

## 许可

[MPL-2.0](LICENSE)
