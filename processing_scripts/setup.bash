#!/bin/bash

for full_filename in bags/*/*.bag; do
    base_filename=$(basename -- "$full_filename")
    filename="${base_filename%.*}"
    dir="$(dirname $full_filename)"
    dir+="/"
    new_dir="$dir$filename"
    echo $new_dir
    if [ ! -d $new_dir ]; then
        mkdir -p $new_dir;
    fi
    new_dir+="/"
    mv $full_filename "$new_dir$base_filename" 
done