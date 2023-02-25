$start_time = Get-Uptime
Write-Output $start_time

python .\.github\workflows\get_info.py -env

if (-Not (Test-Path -Path "./.github/workflows/env.ps1"))
{
    Throw "No env file found as ./github/workflows/env.ps1 !"
}

./.github/workflows/env.ps1

cd libs
cd Difficult_Rocket_rs
cd src
python3.8 setup.py build
python post_build.py
cd ../../..

$arg = @()
# 输出配置
$arg += @("--standalone")
$arg += @("--output-dir=build/nuitka-win")
$arg += @("--company-name=tool-shenjack-workshop")
$arg += @("--product-name=Difficult-Rocket")
$arg += @("--product-version=$env:DR_version")
$arg += @("--file-version=$env:Build_version")
$arg += @("--file-description=Difficult-Rocket!")
$arg += @("--windows-icon-from-ico=textures/icon.png")
#$arg += @("--macos-app-icon=textures/icon.png")
# 编译器配置
$arg += @("--msvc=latest")
$arg += @("--clang")
$arg += @("--lto=no")
# 数据配置
$arg += @("--include-data-dir=./libs/pyglet=./libs/pyglet")
$arg += @("--include-data-dir=./libs/fonts=./libs/fonts")
$arg += @("--include-data-dir=./textures=./textures")
$arg += @("--include-data-dir=./configs=./configs")
# 编译配置
$arg += @("--show-memory")
$arg += @("--show-progress")
$arg += @("--assume-yes-for-download")
python3.8.exe -m nuitka $arg $args DR.py

$end_time = Get-Uptime
$out = $end_time.TotalMilliseconds - $start_time.TotalMilliseconds
Write-Output $end_time.TotalSeconds $start_time.TotalSeconds $out s
Write-Output $start_time $end_time
Write-Output "--clang --lto=no and $args"
Copy-Item .\libs\pyglet\ .\build\nuitka-win\DR.dist -Recurse
# --include-data-dir=./libs/pyglet=./pyglet
# --run
# --disable-ccache
