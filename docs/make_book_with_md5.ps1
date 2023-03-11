mdbook build .
Copy-Item book/README-en.html book/html/README-en.html
rm md5.txt
rm index.html
Get-ChildItem -Recurse -Path book\* | ?{$_.PsIsContainer -eq $false} | Get-FileHash -Algorithm MD5 >> .\md5.txt