
# DR 构建 更新日志

- 最新构建版本号
  - build_version: 2.1.2.0

## 20230708 build 2.1.2.0

### 修改

- 同步了 `lib-not-dr` 的修改
  - `NuitkaCompiler`
    - 添加了 `run_after_build` 选项
      - `--run`
    - 添加了 `compat_nuitka_version` 选项
      - 目前是 `1.7.1`

## 20230630 build 2.1.1.0

### 修改

- 现在本地构建会根据系统名称修改输出目录
  - 例如
    - 在 `Windows` 上构建会输出到 `build\nuitka-windows`
  - Now the local build will modify the output directory according to the system name
    - For example
      - Build on `Windows` will output to `build\nuitka-windows`

## 20230611 build 2.1.0.0

### 添加

- 现在会在每个平台上自动排除其他平台的 `pyglet` 兼容模块
  - 例如
    - 在 `Windows` 上 `--no-follow-import` `pyglet.libs.x11`
  - 大幅提升编译效率
  - 缩短编译时间
  - Now `pyglet` compatibility modules for other platforms will be automatically excluded on each platform
    - For example
      - `--no-follow-import` `pyglet.libs.x11` on `Windows`
    - Greatly improve compilation efficiency
    - Shorten compilation time

## 20230609 build 2.0.0.0

### Breaking Change

- 将构建脚本生成方式改为通过 `libs/utils/nuitka.py` 生成
  - Change the way the build script is generated to generate it through `libs/utils/nuitka.py`
- GitHub Actions 也使用相同脚本构建
  - GitHub Actions also uses the same script to build

## 202306 build 1.3.0.0

- 修改
  - 向 `bifollow-import-to` 添加 `pydoc`
