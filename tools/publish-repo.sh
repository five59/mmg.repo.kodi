#!/bin/bash
SRC=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
SRC=$(dirname "${SRC}")"/web/"
DST="andrew@s17985321.onlinehome-server.com:/var/www/sites/com_marconimedia_kodi"
echo "Synchronizing:"
echo "--> SRC: ${SRC}"
echo "--> DST: ${DST}"
rsync -avzhe ssh --progress --delete "${SRC}" "${DST}"
