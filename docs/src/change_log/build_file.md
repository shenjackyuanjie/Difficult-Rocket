
# DR 构建 更新日志

- 最新构建版本号
  - build_version: 1.3.0.0

## 20230611 build 2.1.0.0

### 添加

- 现在会在每个平台上自动排除其他平台的 `pyglet` 兼容模块
  - 例如
    - 在 `Windows` 上 `--no-follow-import` `pyglet.libs.x11`
  - 大幅提升编译效率
  - 缩短编译时间

## 20230609 build 2.0.0.0

### Breaking Change

- 将构建脚本生成方式改为通过 `libs/utils/nuitka.py` 生成
- GitHub Actions 也使用相同脚本构建

## 202306 build 1.3.0.0

- 修改
  - 向 `bifollow-import-to` 添加 `pydoc`
