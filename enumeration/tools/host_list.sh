#!/bin/bash
#Takes a list of URLs (without trailing slashes) or domains and runs the host command on them, sorting them by IP.
#strip=$(cat $1|sed 's/https\?:\/\///')
cat $1| while read line; do host "$line"; done |grep -E "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b"|sort -n -t " " -k 4
