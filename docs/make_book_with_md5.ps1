mdbook build .
Copy-Item book/README-en.html book/html/README-en.html
Remove-Item md5.txt
Remove-Item index.html
Get-ChildItem -Recurse -Path book\* | Where-Object{$_.PsIsContainer -eq $false} | Get-FileHash -Algorithm MD5 >> .\md5.txt