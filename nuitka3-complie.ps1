$start_time = Get-Uptime
Write-Output $start_time

python .\.github\workflows\get_info.py -env

if (-Not (Test-Path -Path "./.github/workflows/env.ps1"))
{
    Throw "No env file found as ./github/workflows/env.ps1 !"
}

./.github/workflows/env.ps1

$arg = @()
# 输出配置
$arg += @("--standalone")
$arg += @("--output-dir=build/nuitka1")
$arg += @("--company-name=tool-shenjack-workshop")
$arg += @("--product-name=Difficult-Rocket")
$arg += @("--product-version=$env:DR_version")
$arg += @("--file-version=$env:Build_version")
$arg += @("--file-description=Difficult-Rocket!")
$arg += @("--windows-icon-from-ico=textures/icon.png")
$arg += @("--macos-app-icon=textures/icon.png")
# 编译器配置
$arg += @("--msvc=latest")
$arg += @("--clang")
$arg += @("--lto=no")
# 包配置
$arg += @("--nofollow-import-to=objprint,pillow,PIL,pyglet")
# 数据配置
$arg += @("--include-data-dir=./libs/pyglet=./pyglet")
$arg += @("--include-data-dir=./libs/fonts=./libs/fonts")
$arg += @("--include-data-dir=./textures=./textures")
$arg += @("--include-data-dir=./configs=./configs")
# 编译配置
$arg += @("--jobs=24")
$arg += @("--show-memory")
$arg += @("--show-progress")
$arg += @("--assume-yes-for-download")
python3.8.exe -m nuitka $arg $args DR.py

$end_time = Get-Uptime
$out = $end_time.TotalMilliseconds - $start_time.TotalMilliseconds
Write-Output $end_time.TotalSeconds $start_time.TotalSeconds $out s
Write-Output $start_time $end_time
Write-Output "--jobs=24 --mingw64 --lto=no and $args"
# --include-data-dir=./libs/pyglet=./pyglet
# --run
# --disable-ccache
