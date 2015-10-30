## Active Information Gathering

1. ###DNS Enumeration

	DNS offers a variety of information about public (and sometimes private!) organization servers, such as IP addresses, server names, and server functionality.

	- #### Interacting with a DNS Server

		```Bash
 		host -t ns megacorpone.com           # -t : type , ns: dns
		host -t mx megacorpone.com           # mx : mail server
		```

	- ####Automating lookups

		we have some initial data from the megacorpone.com domain, we can continue to use additional DNS queries to discover more host names and IP addresses belonging to megacorpone.com.

		```Bash
		host www.megacorpone.com             # we will found that it has an ip
		host idontexist.megacorpone.com      # this is not found
		```

	- ####Forward Lookup Brute Force

		Taking the previous concept a step further, we can automate the Forward DNS Lookup of common host names using the host command and a Bash script.

		```shell
		echo www > list.txt
		echo ftp >> list.txt
		echo mail >> list.txt
		echo owa >> list.txt
		echo proxy >> list.txt
		echo router >> list.txt
		echo api >> list.txt
		for ip in $(cat list.txt);do host $ip.megacorpone.com;done
		```

	- ####Reverse Lookup Brute Force

		If the DNS administrator of megacorpone.com configured PTR records for the domain, we might find out some more domain names that were missed during the forward lookup brute-force phase.

		```shell
		for ip in $(seq 155 190);do host 50.7.67.$ip;done | grep -v "not found"
		# grep -v :: --invert-match
		```

	- ####DNS Zone Transfers

		- A zone transfer is similar to a database replication act between related DNS servers.
		- This process includes the copying of the zone file from a master DNS server to a slave server.
		- The zone file contains a list of all the DNS names configured for that zone. Zone transfers should usually be limited to authorized slave DNS servers.

		```shell
		host -l megacorpone.com ns1.megacorpone.com   # ns1 refused us our zone transfer request
		# -l :: list all hosts in a domain
		host -l megacorpone.com ns2.megacorpone.com
		# The result is a full dump of the zone file for the megacorpone.com domain,
		# providing us a convenient list of IPs and DNS names for the megacorpone.com domain.
		```

		- Now Lets automate the process:

			- To get the name servers for a given domain in a clean format, we can issue the following command.

				```shell
				host -t ns megacorpone.com | cut -d " " -f 4
				# -d :: --delimiter=DELIM ;
				# -f ::  --fields=LIST select only these fields on each line;
				````

			- Taking this a step further, we could write the following simple Bash script to automate the procedure of discovering and attempting a zone transfer on each DNS server found.

				```shell
				# /bin/bash
				# Simple Zone Transfer Bash Script
				# $1 is the first argument given after the bash script
				# Check if argument was given, if not, print usage
				if  [-z "$1" ]; then
				echo "[*] Simple Zone transfer script"
				echo "[*] Usage : $0 <domain name> "
				exit 0
				fi

				# if argument was given, identify the DNS servers for the domain
				for server in $(host ­-t ns $1 | cut ­-d" " ­-f4);do
				# For each of these servers, attempt a zone transfer
				host -l $1 $server | grep "has address"
				done
				```

				Running this script on megacorpone.com should automatically identify both name servers and attempt a zone transfer on each of them

				```shell
				root@kali:~# chmod 755 dns-­-axfr.sh
				root@kali:~# ./dns-­-axfr.sh megacorpone.com
				```

	- ####Relevant Tools in Kali Linux

		- ####DNSRecon

			```shell
			dnsrecon -d megacorpone.com -t axfr
			# -d :: domain
			# -t :: type of Enumeration to perform
			# axfr :: test all ns servers for zone transfer
			```

		- ####DNSEnum

			```
			dnsenum zonetransfer.me
			```

2. ###Port Scanning

	Port scanning is the process of checking for open TCP or UDP ports on a remote machine.

	> **Please note that port scanning is illegal in many countries and should not be performed outside the labs.**

	- ####Connect Scanning

		- The simplest TCP port scanning technique, usually called CONNECT scanning, relies on the three-way TCP handshake26 mechanism.

		- Connect port scanning involves attempting to complete a three-way handshake with the target host on the specified port(s).
		- If the handshake is completed, this indicates that the port is open.

		```shell
		# TCP Netcat port scan on ports 3388-3390
		nc -nvv -w 1 -z 10.0.0.19 3388-3390
		# -n :: numeric only ip adressess no DNS
		# -v :: verboose use twice to be more verboose
		# -w :: (secs) timeout for connects and final net reads
		# -z :: zero I/O mode (used for scanning)
		```

	- ####Stealth / SYN Scanning

		- SYN scanning, or stealth scanning, is a TCP port scanning method that involves sending SYN packets to various ports on a target machine without completing a TCP handshake.
		- If a TCP port is open, a SYN-ACK should be sent back from the target machine, informing us that the port is open, without the need to send a final ACK back to the target machine.

		- With early and primitive firewalls, this method would often bypass firewall logging, as this logging was limited to completed TCP sessions.
		-  This is no longer true with modern firewalls, and the term stealth is misleading. Users might believe their scans will somehow not be detected, when in fact, they will be.

	- ####UDP Scanning

		```shell
		nc -nv -u -z -w 1 10.0-0.19 160-162
		# -u :: UDP mode
		```

	- ####Common Port Scanning Pitfalls

		- UDP port scanning is often unreliable, as firewalls and routers may drop ICMP packets. This can lead to false positives in your scan, and you will regularly see UDP port scans showing all UDP ports open on a scanned machine.
		- Most port scanners do not scan all available ports, and usually have a preset list of “interesting ports” that are scanned.
		- People often forget to scan for UDP services, and stick only to TCP scanning, thereby seeing only half of the equation.

	- ###Port Scanning with Nmap

		- ####Accountability for Your Traffic

			- A default nmap TCP scan will scan the 1000 most popular ports on a given machine.

			```shell
			# We’ll scan one of my local machines while monitoring the amount
			# of traffic sent to the specific host using iptables.
			iptables -I INPUT 1 -s 10.0.0.19 -j ACCEPT
			iptables -I OUTPUT 1 -d 10.0.0.19 -j ACCEPT
			iptables -Z
			# -I :: insert in chain as rulenum ( default 1=first)
			# -s :: source (address)
			# -j :: jump target for the rulw
			# -Z :: ??

			nmpap -sT 10.0.0.9
			iptables -vn -L
			iptables -Z
			# -sT :: TCP Connect Scan
			# -v :: Display more information in the output
			# -L :: List the current filter rules.

			nmap -sT -p 1-65635 10.0.0.19
			iptables -vn -L
			# -p :: port range
			```

			- This default 1000 port scan has generated around 72KB of traffic.
			-  A similar local port scan explicitly probing all 65535 ports would generate about 4.5 MB of traffic, a significantly higher amount.
			- However, this full port scan has discovered two new ports that were not found by the default TCP scan: ports 180 and 25017.

			**Full nmap scan of a class C network (254 hosts) would result in sending over 1000 MB of traffic to the network.**

			__So, if we are in a position where we can’t run a full port scan on the network, what can we do?__

		- ####Network Sweeping

			- To deal with large volumes of hosts, or to otherwise try to conserve network traffic, we can attempt to probe these machines using Network Sweeping techniques.

			- Machines that filter or block ICMP requests may seem down to a ping sweep, so it is not a definitive way to identify which machines are really up or down.

			```shell
			nmap -sn 192.168.11.200-250
			# -sn :: ping scan
			# using the grep command can give you output that’s difficult to manage.
			# let’s use Nmap’s “greppable” output parameter (-oG)
			nmap -v -sn 192.168.11.200-250 -oG ping-sweep.txt
			grep Up ping-sweep.txt | cut -d " " -f 2

			# we can sweep for specific TCP or UDP ports (-p) across the network
			nmap ­-p 80 192.168.11.200-250 -oG web-sweep.txt
			grep open web­-sweep.txt |cut ­-d " " -f 2

			# we are conducting a scan for the top 20 TCP ports.
			nmap –sT –A --top­-ports=20 192.168.11.200-250 –oG top­-port-­sweep.txt
			```

			- Machines that prove to be rich in services, or otherwise interesting, would then be individually port scanned, using a more exhaustive port list.

	- ###OS Fingerprinting

		```shell
		# OS fingerprinting (-O parameter).
		nmap -O 10.0.0.19
		```

	- ###Banner Grabbing/Service Enumeration

		Nmap can also help identify services on specific ports, by banner grabbing, and running several enumeration scripts (-sV and -A parameters).

		```shell
		nmap -sV -sT 10.0.0.19
		# -sV :: probe open ports to determine service / version info
		```

	- ###Nmap Scripting Engine (NSE)

		- The scripts include a broad range of utilities, from DNS enumeration scripts, brute force attack scripts, and even vulnerability identification scripts.

		- All NSE scripts can be found in the /usr/share/nmap/scripts directory

		```shell
		nmap 10.0.0.19 --script smb-os-discovery.nse
		# Another useful script is the DNS zone transfer NSE script
		nmap --script=dns-zone-transfer -p 53 ns2.megacorpone.com
		```

3. ###SMB Enumeration

	```
	SMB1   – Windows 2000, XP and Windows 2003.
	SMB2   – Windows Vista SP1 and Windows 2008
	SMB2.1 – Windows 7 and Windows 2008 R2
	SMB3   – Windows 8 and Windows 2012.
	```

	- #### Scanning for the NetBIOS Service

		- The SMB NetBIOS32 service listens on TCP ports 139 and 445, as well as several UDP ports.

			```shell
			nmap -v -p 139,445 -oG smb.txt 192.168.11.200-254
			```

		- There are other, more specialized, tools for specifically identifying NetBIOS information

			```
			nbtscan -r 192.168.11.0/24
			```

	- #### Null Session Enumeration

		- A null session refers to an unauthenticated NetBIOS session between two computers. This feature exists to allow unauthenticated machines to obtain browse lists from other Microsoft servers.

		- A null session also allows unauthenticated hackers to obtain large amounts of information about the machine, such as password policies, usernames, group names, machine names, user and host SIDs.

		- This Microsoft feature existed in SMB1 by default and was later restricted in subsequent versions of SMB.

		```
		enum4linux -a 192.168.11.227
		```

	- #### Nmap SMB NSE Scripts

		```shell
		# These scripts can be found in the /usr/share/nmap/scripts directory
		ls -l /usr/share/nmap/scripts/smb*
		# We can see that several interesting Nmap SMB NSE scripts exist,, such as OS discovery
		# and enumeration of various pieces of information from the protocol
		nmap -v -p 139, 445 --script=smb-os-discovery 192.168.11.227
		# To check for known SMB protocol vulnerabilities,
		# you can invoke the nmap smb-check-vulns script
		nmap -v -p 139,445 --script=smb-check-vulns --script-args=unsafe=1 192.168.11.201
		```

	- #### SMTP Enumeration

		- mail servers can also be used to gather information about a host or network.
		- SMTP supports several important commands, such as VRFY and EXPN.
		- A VRFY request asks the server to verify an email address
		- while EXPN asks the server for the membership of a mailing list.
		- These can often be abused to verify existing users on a mail server, which can later aid the attacker.

		```shell
		# This procedure can be used to help guess valid usernames.
		nc -nv 192.168.11.215 25
		```

		- Examine the following simple Python script that opens a TCP socket, connects to the SMTP server, and issues a VRFY command for a given username.

		```python
		#!/usr/bin/python
		import socket
		import sys
		if len(sys.argv) != 2:
			print "Usage: vrfy.py <username>"
			sys.exit(0)
		# Create a Socket
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Connect to the Server
		connect=s.connect(('192.168.11.215',25))
		# Receive the banner
		banner=s.recv(1024)
		print banner
		# VRFY a user
		s.send('VRFY' + sys.argv[1] + '\r\n')
		result=s.recv(1024)
		print result
		# Close the socket
		s.close()
		```
	- ### SNMP Enumeration (Simple Network Management Protocol)

		- SNMP is based on UDP, a simple, stateless protocol, and is therefore susceptible to IP spoofing, and replay attacks.
		- In addition, the commonly used SNMP protocols 1, 2, and 2c offer no traffic encryption, meaning SNMP information and credentials can be easily intercepted over a local network.
		- For all these reasons, SNMP is another of our favorite enumeration protocols.
		---

		- ### MIB Tree (SNMP Management Information Base)

			- (MIB) is a database containing information usually related to network management.
			- The database is organized like a tree, where branches represent different organizations or network functions. The leaves of the tree (final endpoints) correspond to specific variable values that can then be accessed, and probed, by an external user.
			- [Read more about the MIB](http://www-01.ibm.com/support/knowledgecenter/ssw_aix_53/com.ibm.aix.progcomm/doc/progcomc/mib.htm%23jkmb0ria)
		- ### Scanning for SNMP

			```shell
			nmap -sU --open -p 161 192.168.11.200-254 -oG mega-snmp.txt
			# -sU :: UDP scan
			```

			- Alternatively, we can use a tool such as __onesixtyone__, which will check for given community strings against an IP list, allowing us to brute force various community strings.

			```shell
			echo public > community
			echo private >> community
			echo manager >> community
			for ip in $(seq 200 254);do echo 192.168.11.$ip;done > ips
			onesixtyone -c community i ips
			```

			Once these SNMP services are found, we can start querying them for specific MIB data that might be interesting to us.

		- ### Windows SNMP Enumeration Example

			- We can probe and query SNMP values using a tool such as __snmpwalk__ provided we at least know the SNMP read-only community string, which in most cases is “public”.
			- Using some of the MIB values provided above, we could attempt to enumerate their corresponding values.
			- Try out the following examples against a known machine in the labs, which has a Windows SNMP port exposed with the community string “public”.

			```shell
			# Enumerating the Entire MIB Tree
			snmpwalk  c public -v1 192.168.11.219

			# Enumerating Windows Users:
			snmpwalk -c public -v1 192.168.11.204 1.3.6.1.4.1.77.1.2.25

			# Enumerating Running Windows Processes:
			snmpwalk -c public -v1 192.168.11.204 1.3.6.1.2.1.25.4.2.1.2

			# Enumerating Open TCP Ports:
			snmpwalk -c public -v1 192.168.11.204 1.3.6.1.2.1.6.13.1.3

			# Enumerating Installed Software:
			snmpwalk -c public v1 192.168.11.204 1.3.6.1.2.1.25.6.3.1.2
			```

			- try to Use __snmpwalk__ and __snmpcheck__ to gather information about the discovered targets.
