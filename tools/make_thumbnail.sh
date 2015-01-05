#!/bin/bash

function prep () {
    if [ -f "${1}" ]
    then
        echo "Converting ${1}..."
        convert ${1} -gravity center -background white -extent 256x256 ./dest/${1}.png
    else
        echo "${1} is not a file."
    fi
}

for f in $(find .); do
    prep $f
done
