# SNMP Enumeration (Simple Network Management Protocol)

## Fix SNMP output values so they are human readable

```ShellSession
apt-get install snmp-mibs-downloader download-mibs
echo "" > /etc/snmp/snmp.conf
```

## Scanning for SNMP

### Using nmap

```ShellSession
root@kali:~# nmap -sU -v --open -p 161 192.168.1.12
   Note: SNMP is using UDP not TCP
```

### Using onesixtyone

```ShellSession
root@kali:~# echo public > /tmp/community.txt
root@kali:~# echo private >> /tmp/community.txt
root@kali:~# echo manager >> /tmp/community.txt
root@kali:~# echo 192.168.1.12 > /tmp/ip.txt
root@kali:~# onesixtyone -c /tmp/community.txt -i /tmp/ip.txt
```

## Windows SNMP Enumeration Example

```ShellSession
root@kali:~# snmpwalk -c puplic -v1 192.168.1.12
```

## SNMP Enumeration Commands

```ShellSession
snmpcheck -t $ip -c public

snmpwalk -c public -v1 $ip 1|

grep hrSWRunName|cut -d\* \* -f

snmpenum -t $ip

onesixtyone -c names -i hosts
```

## SNMPv3 Enumeration

```ShellSession
nmap -sV -p 161 --script=snmp-info $ip/24
```

## Automate the username enumeration process for SNMPv3:

```ShellSession
apt-get install snmp snmp-mibs-downloader
wget https://raw.githubusercontent.com/raesene/TestingScripts/master/snmpv3enum.rb
```

## SNMP Default Credentials

```ShellSession
/usr/share/metasploit-framework/data/wordlists/snmp\_default\_pass.tx
```
