
# DR SDK 更新日志

- 最新版本号
  - DR sdk: 0.8.1.0

## DR sdk 0.8.1.0

### 删除

- `api.types.SR1`
  - 移动到 `dr_game` 中

### 添加

- `api.types`
  - 添加 `Version` (`libs.MCDR.version.Version`)

### 修复 Bug

- 自带的 `console` 类在 `get_command` 时 没有检查是否为空
