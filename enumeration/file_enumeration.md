# File Enumeration

- Find UID 0 files root execution

```ShellSession
/usr/bin/find / -perm -g=s -o -perm -4000 ! -type l -maxdepth 3 -exec ls -ld {} \\\\; 2>/dev/null
```

- Get handy linux file system enumeration script (/var/tmp)

```ShellSession
wget <https://highon.coffee/downloads/linux-local-enum.sh>

chmod +x ./linux-local-enum.sh

./linux-local-enum.sh
```

- Find executable files updated in August

```ShellSession
find / -executable -type f 2> /dev/null | egrep -v "^/bin|^/var|^/etc|^/usr" | xargs ls -lh | grep Aug
```

- Find a specific file on linux

```ShellSession
find /. -name suid\\\*\\
```

- Find all the strings in a file

```ShellSession
strings <filename>
```

- Determine the type of a file

```ShellSession
file <filename>
```

