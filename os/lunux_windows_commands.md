
[Source](https://www.lemoda.net/windows/windows2unix/windows2unix.html "Permalink to Windows and Unix command line equivalents")

# Windows and Unix command line equivalents

This lists similar commands between Windows and Unix command lines.

To get help on a Windows command, use the `/?` option, for example `date /?`.

| ----- |
| Windows command |  Unix command |  Notes |
| `arp` |  [`arp][1]` |   |
| `assign` |  [`ln][2]` |  Create a file link |
| `assign` |  [`ln][2] -s` |  On Unix, a directory may not have multiple links, so instead a symbolic link must be created with `ln -s`. |
| `assoc` |  [`file][3]` |   |
| `at` |  [`at][4]
[batch][5]
[cron][6]` |   |
| `attrib` |  [`chown][7]
[chmod][8]` |  Sets ownership on files and directories |
| `cd` |  [`cd][9]` |  On Windows, `cd` alone prints the current directory, but on Unix `cd` alone returns the user to his home directory. |
| `cd` |  [`pwd][10]` |  On Windows, **cd** alone prints the current directory. |
| `chkdsk` |  [`fsck][11]` |  Checks filesystem and repairs filesystem corruption on hard drives. |
| `cls` |  [`clear][12]` |  Clear the terminal screen |
| `copy` |  [`cp][13]` |   |
| `date
time` |  [`date][14]` |  `Date` on Unix prints the current date and time. `Date` and `time` on Windows print the date and time respectively, and prompt for a new date or time. |
| `del` |  [`rm][15]` |   |
| `deltree` |  [`rm][15] -r` |  Recursively deletes entire directory tree |
| `dir` |  [`ls][16]` |  "dir" also works on some versions of Unix. |
| `doskey /h
F7 key` |  [`history][17]` |  The Unix `history` is part of the Bash shell. |
| `edit` |  `vi
emacs
etc.` |  `edit` brings up a simple text editor in Windows. On Unix, the environment variable `EDITOR` should be set to the user's preferred editor. |
| `exit` |  `[exit][18]
Control-D` |  On Unix, pressing the control key and D simultaneously logs the user out of the shell. |
| `explorer` |  `nautilus
etc.` |  The command `explorer` brings up the file browser on Windows. |
| `fc` |  `[diff][19]` |   |
| `find` |  `[grep][20]` |   |
| `ftp` |  `[ftp][21]` |   |
| `help` |  `[man][22]` |  "help" by itself prints all the commands |
| `hostname` |  `[hostname][23]` |   |
| `ipconfig /all` |  `[ifconfig][24] -a` |  The /all option lets you get the MAC address of the Windows PC |
| `mem` |  `[top][25]` |  Shows system status |
| `mkdir` |  `[mkdir][26]` |   |
| `more` |  `[more][27]
[less][28]` |   |
| `move` |  `[mv][29]` |   |
| `net session` |  `[w][30]
[who][31]` |   |
| `net statistics` |  `[uptime][32]` |   |
| `nslookup` |  `[nslookup][33]` |   |
| `ping` |  `[ping][34]` |   |
| `print` |  `lpr` |  Send a file to a printer. |
| `reboot
shutdown -r` |  `[shutdown][35] -r` |   |
| `regedit` |  `edit /etc/*` |  The Unix equivalent of the Windows registry are the files under `/etc` and `/usr/local/etc`. These are edited with a text editor rather than with a special-purpose editing program. |
| `rmdir` |  `[rmdir][36]` |   |
| `rmdir /s` |  `[rm][15] -r` |  Windows has a y/n prompt. To get the prompt with Unix, use `rm -i`. The `i` means "interactive". |
| `set` |  `[env][37]` |

`Set` on Windows prints a list of all environment variables. For individual environment variables, set  is the same as echo $ on Unix.

 |
| `set Path` |  `echo $PATH` |  Print the value of the environment variable using `set` in Windows. |
| `shutdown` |  `[shutdown][35]` |  Without an option, the Windows version produces a help message |
| `shutdown -s` |  `[shutdown][35] -h` |  Also need -f option to Windows if logged in remotely |
| `sort` |  `[sort][38]` |   |
| `start` |  `&` |  On Unix, to start a job in the background, use `command &`. On Windows, the equivalent is `start command`. See [How to run a Windows command as a background job like Unix ?][39]. |
| `systeminfo` |  `[uname][40] -a` |   |
| `tasklist` |  `[ps][41]` |  "tasklist" is not available on some versions of Windows. See also [this article on getting a list of processes in Windows using Perl][42] |
| `title` |  `?` |  In Unix, changing the title of the terminal window is possible but complicated. Search for "change title xterm". |
| `tracert` |  `[traceroute][43]` |   |
| `tree` |  `[find][44]
[ls][16] -R` |  On Windows, use tree | find "string" |
| `type` |  `[cat][45]` |   |
| `ver` |  `[uname][40] -a` |   |
| `xcopy` |  `[cp][13] -R` |  Recursively copy a directory tree |

Links open in a separate window. The links on the Unix commands go to an online version of the FreeBSD manual page.

[1]: http://nxmnpg.lemoda.net/1/arp
[2]: http://nxmnpg.lemoda.net/1/ln
[3]: http://nxmnpg.lemoda.net/1/file
[4]: http://nxmnpg.lemoda.net/1/at
[5]: http://nxmnpg.lemoda.net/1/batch
[6]: http://nxmnpg.lemoda.net/1/cron
[7]: http://nxmnpg.lemoda.net/1/chown
[8]: http://nxmnpg.lemoda.net/1/chmod
[9]: http://nxmnpg.lemoda.net/1/cd
[10]: http://nxmnpg.lemoda.net/1/pwd
[11]: http://nxmnpg.lemoda.net/1/fsck
[12]: http://nxmnpg.lemoda.net/1/clear
[13]: http://nxmnpg.lemoda.net/1/cp
[14]: http://nxmnpg.lemoda.net/1/date
[15]: http://nxmnpg.lemoda.net/1/rm
[16]: http://nxmnpg.lemoda.net/1/ls
[17]: http://nxmnpg.lemoda.net/1/history
[18]: http://nxmnpg.lemoda.net/1/exit
[19]: http://nxmnpg.lemoda.net/1/diff
[20]: http://nxmnpg.lemoda.net/1/grep
[21]: http://nxmnpg.lemoda.net/1/ftp
[22]: http://nxmnpg.lemoda.net/1/man
[23]: http://nxmnpg.lemoda.net/1/hostname
[24]: http://nxmnpg.lemoda.net/1/ifconfig
[25]: http://nxmnpg.lemoda.net/1/top
[26]: http://nxmnpg.lemoda.net/1/mkdir
[27]: http://nxmnpg.lemoda.net/1/more
[28]: http://nxmnpg.lemoda.net/1/less
[29]: http://nxmnpg.lemoda.net/1/mv
[30]: http://nxmnpg.lemoda.net/1/w
[31]: http://nxmnpg.lemoda.net/1/who
[32]: http://nxmnpg.lemoda.net/1/uptime
[33]: http://nxmnpg.lemoda.net/1/nslookup
[34]: http://nxmnpg.lemoda.net/1/ping
[35]: http://nxmnpg.lemoda.net/1/shutdown
[36]: http://nxmnpg.lemoda.net/1/rmdir
[37]: http://nxmnpg.lemoda.net/1/env
[38]: http://nxmnpg.lemoda.net/1/sort
[39]: http://www.tomshardware.com/forum/34598-45-windows-command-background-unix
[40]: http://nxmnpg.lemoda.net/1/uname
[41]: http://nxmnpg.lemoda.net/1/ps
[42]: https://www.lemoda.net/perl/win-ps-list/win-ps-list.html
[43]: http://nxmnpg.lemoda.net/1/traceroute
[44]: http://nxmnpg.lemoda.net/1/find
[45]: http://nxmnpg.lemoda.net/1/cat

