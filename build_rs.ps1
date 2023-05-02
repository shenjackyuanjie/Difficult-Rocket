Set-Location .\mods\dr_game\Difficult_Rocket_rs\src

Write-Output $args[0]

$do = 0

if ("38" -notin $args -and "39" -notin $args -and "310" -notin $args -and "311" -notin $args) {
    $do = 1
}

cargo fmt

if ($do -or "38" -in $args) {
    python3.8 setup.py build
}
if ($do -or "39" -in $args) {
    python3.9 setup.py build
}
if ($do -or "310" -in $args) {
    python3.10 setup.py build
}
if ($do -or "311" -in $args) {
    python3.11 setup.py build
}

python3.8 post_build.py

Set-Location ..\..\..\..\
