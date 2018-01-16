#!/bin/bash
echo ""
go run main.go -u $1 -t 25 -k -w ../SecLists-master/Discovery/Web_Content/raft-large-directories-lowercase.txt -s 200 -fw -q -e
go run main.go -u $1 -t 25 -k -w ../SecLists-master/Discovery/Web_Content/raft-large-files-lowercase.txt -s 200 -fw -q -e
#go run main.go -u $1 -t 50 -k -w ../Top100000-RobotsDisallowed2.txt -s 200 -fw
echo ""
