$start_time = Get-Uptime
Write-Output $start_time

$arg = @()
# 输出配置
$arg += @("--standalone")
$arg += @("--output-dir=build/nuitka1")
$arg += @("--company-name=tool-shenjack-workshop")
$arg += @("--product-name=Difficult-Rocket")
$arg += @("--product-version=0.6.4")
$arg += @("--file-version=0.0.0.1")
$arg += @("--file-description=Difficult-Rocket!")
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
