# Difficult Rocket

Readme 请查看 [dr.shenjack.top](https://dr.shenjack.top/main/readme)

Readme please check out [dr.shenjack.top](https://dr.shenjack.top/main/readme-en)

## 下面是一个 老的, 未同步的 readme
## below is an old, unsynchronized readme

# Difficult Rocket

[中文](./README.md) | English

- [GitHub](https://github.com/shenjackyuanjie/Difficult-Rocket)
- [Gitee](https://gitee.com/shenjackyuanjie/Difficult-Rocket)
- [AtomGit](https://atomgit.com/shenjackyuanjie/Difficult-Rocket)

- [Discord](https://discord.gg/kWzw2JrG6M)
- [Kook](https://kook.top/sRPjFG)

> Note: This repo will only publish `DR SDK` updates, `DR game` updates will be published [here](https://github.com/shenjackyuanjie/DR-game).

[![996.icu](https://img.shields.io/badge/996.icu-996.icu-red.svg)](https://996.icu)
[![semver](https://img.shields.io/badge/SemVer-2.0.0-blue.svg)](https://Semver.org/)
[![python-3.8.10](https://img.shields.io/badge/编写于_Python_版本-3.8.10-blue.svg)](https://Python.org)
[![pyglet-2.x](https://img.shields.io/badge/编写于_Pyglet_版本-2.x-blue.svg)](https://pyglet.org)
[![support python 3.8~12](https://img.shields.io/badge/Python-_3.8_~_3.12_-blue.svg)](https://Python.org)

## Version

[About Versions](src/version.md)

[![release version](https://img.shields.io/badge/Release-0.9.2.0-blue.svg)](https://github.com/shenjackyuanjie/Difficult-Rocket/releases)
[![pre version](https://img.shields.io/badge/Pre_Release-0.9.2.0-blue.svg)](https://github.com/shenjackyuanjie/Difficult-Rocket/releases)
[![devlo version](https://img.shields.io/badge/Devloping-0.9.3-blue.svg)](https://github.com/shenjackyuanjie/Difficult-Rocket/releases)

[![language badge](https://stats.deeptrain.net/repo/shenjackyuanjie/Difficult-Rocket?theme=dark)](https://stats.deeptrain.net/repo/shenjackyuanjie/Difficult-Rocket?theme=dark)

[DR sdk latest Action build](https://nightly.link/shenjackyuanjie/Difficult-Rocket/workflows/nuitka/main)

[DR rs latest Action build](https://nightly.link/shenjackyuanjie/Difficult-Rocket/workflows/dr_rs/main)

## Introduction

Difficult-rocket is a Simple Rocket liked game build with Python (shorten as "rocket simulator"). It is lighter than Vanilla SR.

[Plan feature list](src/plan_features/README.md)

[YouTrack](https://difficult-rocket.youtrack.cloud/projects/8dafd498-59c0-4ce7-9900-d9292e9ed1f0)

[Update logs](src/change_log/readme.md)

## Run

### 1. Clone

```bash title="clone.sh"
mkdir DR
cd DR
git clone https://github.com/shenjackyuanjie/Difficult-Rocket.git
# or
git clone https://gitee.com/shenjackyuanjie/Difficult-Rocket.git
# or
git clone git@github.com:shenjackyuanjie/Difficult-Rocket.git
```

### 2. Install requirements

```bash title="install.sh"
python gen_require.py 0
python -m pip install -r requirements.txt
git submodule update --init --recursive
cd libs
python -m pip install ./lib_not_dr
python -m pip install ./pyglet
```

### 3. Run

```bash title="run.sh"
python DR.py
```

## Environment

> The developing environment used Python `3.8.10`, but `3.8+` is also available.
>
> After `3.8` EOL, `3.11` will be used as the developing environment.
>
> We use 3.8 for now because it's the last version officially support Windows 7.

- `Develop platform 1 - Windows 10 x64 22H2`
  - Python `3.8.18+`
    - `Python 3.8.18+ (heads/3.8:7f59c4c1d4, Aug 26 2023, 00:20:02) [MSC v.1900 64 bit (AMD64)] on win32`
  - `AMD R5 5800X`
  - `AMD RX 558 8G`

## Required Python Modules

> python gen_require.py [-h] {0,1,2}
> run / build / compile

- `pyglet` (pre-installed V2.x path:`./libs/pyglet`)
- `xmltodict` (pre-installed V0.12.0 path:`./libs/xmltodict`)
- `pyperclip` (pre-installed V1.8.2 path: `./libs/pyperclip`)

## Credits

- Open Source Projects
  - [pyglet](https://github.com/pyglet/pyglet): GUI and graphics
  - tomls
    - `tomlkit`
    - `tomli`
    - `rtoml`
  - `xmltodict`: translate data between xml and dict
  - `pyperclip`: paste board!
  - [rapier2d](https://rapier.rs/) : Phy simulate engine
  - [pyo3](https://pyo3.rs/main) : Rust Python Binding

- Jundroo
  - Thanks you for writing SR this ~~magical~~ fun game

- Main contributors
  - [@shenjackyuanjie](https://github.com/shenjackyuanjie) : Main developer
  - [@sssssssboom](https://github.com/ssssssssboom) : DR game developer
  - [@InfyniteHeap](https://github.com/InfyniteHeap) : DR rs developer
  - [@Rayawa](https://github.com/Rayawa) : Check mistake in docs & some translates
  - [@rouxiao-you](https://github.com/ruoxiao-you) : Translate chinese to English
  - [@Billchyi](https://github.com/Billchyi) : Check mistake in docs
  - [@MSDNicrosoft](https://github.com/MSDNicrosoft) : Optimize code

## Other Links

[Offical Document](https://dr.shenjack.top)

## License

[MPL-2.0](LICENSE)
