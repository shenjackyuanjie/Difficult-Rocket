
$objects = git verify-pack -v .git/objects/pack/pack-aba4bfc55979194c86dbd466c86e57d8199ae7ad.idx | Select-String -Pattern 'chain' -NotMatch | ForEach-Object {$_.Line} | Sort-Object -Property @{Expression={$_.Split(" ")[2]}; Ascending=$false} | Select-Object -First 50

Write-Output "All sizes are in kB. The pack column is the size of the object, compressed, inside the pack file."

$output = "size,pack,SHA,location"
foreach ($y in $objects) {
    # extract the size in bytes
    $size = [int]($y.Split(" ")[4]/1024)
    # extract the compressed size in bytes
    $compressedSize = [int]($y.Split(" ")[5]/1024)
    # extract the SHA
    $sha = $y.Split(" ")[0]
    # find the objects location in the repository tree
    $other = git rev-list --all --objects | Select-String $sha
    $output += "`n${size},${compressedSize},${other}"
}

Write-Output $output | ConvertFrom-Csv -Delimiter "," | Format-Table
Pause
