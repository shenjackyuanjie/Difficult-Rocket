#!/bin/bash
#set -x 
IFS=$'\n';

# 默认值是 10个  可以一次性展示更多 就修改第15行代码  | head -n 30 或者更多
objects=`git verify-pack -v .git/objects/pack/pack-aba4bfc55979194c86dbd466c86e57d8199ae7ad.idx | grep -v chain | sort -k3nr | head -n 50`

echo "All sizes are in kB. The pack column is the size of the object, compressed, inside the pack file."

output="size,pack,SHA,location"
for y in $objects
do
    # extract the size in bytes
    size=$((`echo $y | cut -f 5 -d ' '`/1024))
    # extract the compressed size in bytes
    compressedSize=$((`echo $y | cut -f 6 -d ' '`/1024))
    # extract the SHA
    sha=`echo $y | cut -f 1 -d ' '`
    # find the objects location in the repository tree
    other=`git rev-list --all --objects | grep $sha`
    #lineBreak=`echo -e "\n"`
    output="${output}\n${size},${compressedSize},${other}"
done

echo -e $output | column -t -s ', '
