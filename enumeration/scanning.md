# Scanning

## War Dialers

- War dialers dial a sequence of telephone numbers, attempting to locate modem carriers or a secondary dial tone
- Demon dialers dial a single number to conduct a brute-force attack against passwords
- Often, an unprotected modem provides the easiest method for penetrating a network
- Many recent news stories about hacking voicemail

### WarVOX

- A war-dialing tool
- Install here: https://github.com/rapid7/warvox
- WarVOX war dialing: 1,000 numbers per hour, Traditional modem-based war dialing: 1,000 numbers in approx. 8 hours
- Supports caller ID spoofing
  - Enter a single number for all calls dialed
  - Enter variable number of Xs for pseudo-random source number
  - Enter “SELF” to make caller ID same as dialed number; may bypass PIN authentication in some voicemail systems.
- WarVOX records an MP3 audio file associated with each number dialed and answered, with results stored in a PostgreSQL database
- You can apply a series of signatures to determine what answered., entirely new signatures to match individual human voices
- Modem, fax, voicemail box, and more

### War Dialers - Now What

- So I’ve found a bunch of modems... what do I do now
- Review the war dialer logs and look for familiar login prompts or warning banners
- Connect to each discovered modem Oftentimes, you find a system without a password
  - Old, neglected machine stifi on the network
  - Router
- If there is a user ID/password prompt, guess
  - Make it an educated guess, based on the system
  - What are default accounts/passwords
  - What common things are associated with the target

## War Driving

### Wireless Misconfiguration

- Many wireless access points (base stations) are configured with no security
  - Blank or default SSIDs are common
- By default, most access points broadcast beacon packets with their SSIDs 10 times per second
- Even for those APs configured not to include the SSID in beacons (SSID cloaking), SSIDs are still sent in clear text whenever anyone uses the wireless LAN
  - Therefore, the SSID is, in no way, a security feature
- Various wireless security protocols (WEP and LEAP specifically) have significant flaws
  - Just turning on” security is often not enough protection for sensitive traffic and systems

### Tools for Wireless LAN Discovery

- NetStumbler
  - http://www.netstumbler.com/downloads/
  - windows-bases, problems with winVista, 7 and 8
  - Detects 802.11 a/b/g

- InSSIDER by MetaGeek
  - https://www.metageek.com/products/inssider/
  - Detects 802.11 a/b/g/n
  - Works on XP, Vista, 7, and 8
  - Linux version also available

- Both tools are noisy; they send SSID4ess probe requests and look for probe responses
- Therefore, cannot detect APs that don’t respond to such requests!

### Sniffing

#### Kismet

- It can passively discover access points without ever sending a beacon message. It just sniffs, looking for SSIDs in the messages sent across a network.
- So, even if you disable beacon responses on the access point, Kismet can still detect the APs presence, as long as someone is sending traffic over the wireless LAN.
- The main difference between many Linux-based tools, such as Kismet, and many Windows-based tools is that **many Linux tools have the capability to passively sniff wireless networks**.
- With the proper adapters, Kismet also has the ability to detect other wireless protocols, such as Zigbee

#### Additional tools for sniffing and crypto attacks

- Utilize a traditional sniffer, gathering wireless packets
  - `Tcpdump`, `Wire Shark`, and more War Driving
- Or use a wireless-specific sniffer for better analysis of wireless specific frame data
  - `Omnipeek` (formerly Airopeek), Commercial
    - https://www.savvius.com/product/omnipeek/
- `Aircrack-ng` and `WEPCrack` crack WEP keys
  - https://www.aircrack-ng.org/
  - http://wepcrack.sourceforge.net
- `ASLEAP` (included in kali) by Josh Wright provides a dictionary attack against LEAP authentication
- Josh Wright has released a tool called `CoWPAtty` (in Kali)
  - A dictionary-based cracking tool for pre-shared keys with WPA1 and WPA2
  - Must sniff four-way handshake
  - Cryptographically, WPA is a complex protocol
    - On a modern laptop, crypto routines can try between 10 and 50 guess/encrypt/compares per second
  - Thus, pre-computed encrypted dictionaries are a big help... But, WPA folds SSID into its cryptographic exchange
  - Pre-computed dictionaries are available for
    - The 1000 most common SSIDs (linksys, tsunami, for example) with 172,000 passwords for > 7 Gigs
    - The 1,000 most common SSIDs with 1 million words for > 33 Gigs
- `Easy-Creds` (included in kali) allows an attacker to quickly configure an evil wireless access point that the attacker has full control over.
- `Karmetasploit` is a great function within Metasploit, allowing you to fake access points, capture passwords, harvest data, and conduct browser attacks against clients.

  - Once a client joins imposter network, Karmetasploit includes various services
    - DHCP (of course)
    - DNS: All DNS requests are intercepted, and the attacker’s own IP address is returned
    - POP3: “I’m your mail server. Authenticate to me.”
    - HTTP: “I’m also every server on the entire Internet. Want to talk?”
    - Samba: All Windows file sharing points back to the attacker’s machine
  - Karemetasploit exploits various client software, of course
    - All Metasploit clientside exploits can be configured and launched
    - Hundreds from which to choose
    - Karemetasploit can exploit vulnerable browsers, mail readers, Windows file-sharing clients (such as svchost), and other technologies.

## Network Mapping

### Network Mapping with Nmap/Zenmap

[](cheat_sheets/nmap_quick_reference_guide.pdf)

- By default, to identify which addresses are in use, Nmap sends the following four packets to each address in the target range:
  - ICMP Echo Request
  - TCP SYN to port 443
  - TCP ACK to port 80 (if Nmap is running with UID o)
  - ICMP Timestamp request
- When running without UID o, Nmap sends SYN to port 8o instead of ACK

### How Traditional Traceroute Works

- Traceroute sends packets with small Time to Live (TTL) values
- The Linux traceroute and Windows tracert commands support a -6 option to force IPv6 tracerouting using Hop Limit fields
- IPv4 TTL and IPv6 Hop Limit is the number of hops the packet should go before being discarded
  - An ICMP Time Exceeded message comes back
- Based on the source address of the TTL-exceeded message, you can determine the router for a given hop
- The scanning system increments TfL for each packet to determine each router hop

## Port Scanning

- Current official port numbers can be found at IANA (https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
- There are 2^16 65,536 different TCP ports and 65,536 different UDP ports

Nmap allows for conducting numerous types of scans:

- **Ping sweeps**: Send a variety of packet types (including ICMP Echo Requests, but many others as well).
- **ARP scans**: Identify which hosts are on the same LAN as the machine running Nmap. The ARP scan does not work through a router, because ARP traffic just goes on a single LAN.
- **Connect scans**: Complete the three-way handshake; are slow and easily detected. Because the entire handshake is completed for each port in the scan, the activities are often logged on the target system.
- **SYN scans**: Only send the initial SYN and await the SYN-ACK response to determine if a port is open. The final ACK packet from the attacker is never sent. The result is an increase in performance and a much more stealthy scan. Because most host systems do not log a connection unless it completes the three-way handshake, the scan is less likely to be detected (NOT ANYMORE).
- **ACK scans**: Particularly useful in getting through simple router-based firewalls. If a router allows “established” connections in (and is not using any stateful inspection), an attacker can use ACK scans to send packets into the network. ACK scans are useful for mapping, but not for port scanning.
- **FIN scans**: Send packets with the FIN control bit set in an effort to be stealthy and get through firewalls.
- **FTP Proxy “Bounce Attack” scans**: Bounce an attack off a poorly configured FTP server.
- **“Idle” scans**: This scan type can be used to divert attention, obscuring the attackers location on the network.
- **UDP scanning**: Helps locate vulnerahle UDP services. For most UDP ports, Nmap sends packets with an empty payload. But, for about a dozen specific ports, Nrnap includes an application-appropriate payload for the given port, including UDP port 53 (DNS), 111 (portmapper). 161 (SNMP), etc.
- **Version scanning**: Tries to detemine the version number of the program listening on a discovered port for both TCP and UDP.
- **IPv6 scanning**: Iterates through a series of lPv6 addresses, scanning for target systems and ports, invoked with the “-6” syntax. Today, all Nmap scan types support a -6 option. In older versions of Nmap, IPv6 scans were limited to ping sweeps to identify target host addresses in use, TCP connect scans, and version scans only.
- **RPC scanning**: Identifies which Remote Procedure Call services are offered by the target machine.
- **TCP sequence prediction**: Useful in spooling attacks, as we shall see in a short while.

### Other port scanners

#### Masscan

- TCP port scanner, spews SYN packets asynchronously, scanning entire Internet in under 5 minutes.
- https://github.com/robertdavidgraham/masscan

#### EyeWitness

- Takes screenshots of websites, VNC and RDP servers
- Can be very effective to sort through hundreds of different websites Port Scanning
- Attackers and testers look for default pages, out-of-date servers, RDP sewers which show domains, index-able directories, etc.
- Many vulnerabilities are not necessaiy vulnerabilities which have a Metasploit module
- finding backup files and install scripts on web servers can lead to easy access to external systems
- https://github.com/ChrisTruncer/EyeWitness

#### Remux

- Proof of concept tool to demonstrate scanning through multiple open proxies online
- Revers multiplexes connections
- Browser connects to remux.py
- Rernux.py federates connections through the proxies
- The list of proxies are automatically downloaded at runtime
- You can also specify a list of known good proxies at runtime
- Makes identifying the scanning system very difficult
- When remux.py starts, it is very slow and buggy
  - It slowly learns which proxies are alive and which are no longer active
  - Gets more stable and faster over time

#### Locally checking for listening ports on windows

- In Windows, run `C:\> netstat -na` --> Shows listening TCP/UDP ports
- We can go further
  - `C:\> netstat -nao` --> Showspid
  - `C:\> netstat -nab` --> Shows EXE and all DLLS used
- As a separate download, Microsoft has the Port Reporter tool
  - It periodically generates logs showing port activity
  - Free at http://support.microsoft.com/kb/837243
- For a GUI view of port usage, use `TCPView`

#### Locally checking for listening ports on linux

On Linux/UNIX, you could run `> netstat -nap`
