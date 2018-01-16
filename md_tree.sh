#!/bin/bash

#File: tree-md

tree=$(tree -f --noreport -I '*~|.*|*.png|*.pdf|*.txt|*.jpg|*.svg|*.gif' -L 3 --charset ascii $1 |
       sed -e 's/| \+/  /g' -e 's/[|`]-\+/ */g' -e 's:\(* \)\(\(.*/\)\([^/]\+\)\):\1[\4](\2):g')

printf "# Penetration Testing Study Notes\n\nThis repo contains all my penetration testing study notes, penetration testing tools, scripts, techniques, tricks and also many scripts that I found them useful from all over the internet.\n\n## Table of Contents\n\n${tree}"
