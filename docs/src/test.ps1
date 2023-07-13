
# ls 之后将每一行输出包裹在 ` 里面
echo "<pre>"
Get-ChildItem . | ForEach-Object {
    echo $_
}

echo "</pre>"