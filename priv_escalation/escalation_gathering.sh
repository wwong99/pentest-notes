#Script to gathering information in a privilege escalation

#!/bin/sh
echo Distribution and kernel version
cat /etc/issue
uname -a

echo Mounted filesystems
mount -l

echo Network configuration
ifconfig -a
cat /etc/hosts
arp

echo Development tools availability
which gcc
which g++
which python

echo Installed packages (Ubuntu)
dpkg -l

echo Services
netstat -tulnpe

echo Processes
ps -aux

echo Scheduled jobs
find /etc/cron* -ls 2>/dev/null
find /var/spool/cron* -ls 2>/dev/null

echo Readable files in /etc 
find /etc -user `id -u` -perm -u=r \
 -o -group `id -g` -perm -g=r \
 -o -perm -o=r \
 -ls 2>/dev/null 

echo SUID and GUID writable files
find / -o -group `id -g` -perm -g=w -perm -u=s \
 -o -perm -o=w -perm -u=s \
 -o -perm -o=w -perm -g=s \
 -ls 2>/dev/null 

echo SUID and GUID files
find / -type f -perm -u=s -o -type f -perm -g=s \
 -ls 2>/dev/null

echo Writable files outside HOME
mount -l find / -path “$HOME” -prune -o -path “/proc” -prune -o \( ! -type l \) \( -user `id -u` -perm -u=w  -o -group `id -g` -perm -g=w  -o -perm -o=w \) -ls 2>/dev/null
