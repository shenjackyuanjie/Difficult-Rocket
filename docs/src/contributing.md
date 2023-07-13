# 如何帮助 DR 开发

## 需要准备的工具

1. Powershell 7+
2. Python3.8 +
3. gcc / clang 编译器
4. rust 工具链
5. git

## 安装依赖

1. 确保 Path 下有以下内容
    - `python`
    - `python3.8`
    - 可供 `setuptools-rust` 调用的 rust 工具链
2. 为 Python 安装 [requrements-dev.txt](../requirement-dev.txt) 的依赖
   - `python -m pip install -r requre`
3. 使用 `build_rs.ps1` 尝试编译一次 `DR_rs`
   - `./build_rs.ps1` 38/39/310/311

<!-- cmdrun test.ps1 -->
