# Networking Concepts

<!-- TOC -->

- [Types of networks](#types-of-networks)
- [Physical and Logical topologies](#physical-and-logical-topologies)
  - [Physical topologies](#physical-topologies)
    - [Types of physical topologies](#types-of-physical-topologies)
    - [Star topology](#star-topology)
  - [Logical Topologies](#logical-topologies)
    - [Ethernet](#ethernet)
  - [Token ring and FDDI](#token-ring-and-fddi)
    - [Token ring](#token-ring)
    - [FDDI](#fddi)
    - [Asynchronous Transfer Mode (ATM)](#asynchronous-transfer-mode-atm)
- [Wan Technologies](#wan-technologies)
  - [Frame Relay](#frame-relay)
  - [MPLS (Multi-protocol Label Switching)](#mpls-multi-protocol-label-switching)
  - [ISDN, DSL, Cable Modems](#isdn-dsl-cable-modems)
    - [ISDN](#isdn)
    - [DSL (Digital Subscriber Line)](#dsl-digital-subscriber-line)
    - [Cable modems](#cable-modems)
- [Network Hardware](#network-hardware)
  - [Cabling](#cabling)
  - [Network Tap](#network-tap)
  - [Vampire Tap](#vampire-tap)
- [Network Devices](#network-devices)
- [Network design](#network-design)
- [OSI MODEL](#osi-model)
- [TCP/IP Model](#tcpip-model)
- [How protocol stacks communicate](#how-protocol-stacks-communicate)
- [How TCP packets are created](#how-tcp-packets-are-created)
  - [IP V4 header](#ip-v4-header)
  - [IP V6 header](#ip-v6-header)
  - [IP fragment attacks](#ip-fragment-attacks)
- [Network Addressing](#network-addressing)
  - [Subnet classes](#subnet-classes)
  - [CIDR (ClassLess Inter-Domain Routing)](#cidr-classless-inter-domain-routing)
  - [Broadcast addresses](#broadcast-addresses)
  - [Private addresses](#private-addresses)
  - [IP v6](#ip-v6)
  - [MAC and IP address](#mac-and-ip-address)
  - [ARP (Address Resolution Protocol)](#arp-address-resolution-protocol)
- [Ports and protocols](#ports-and-protocols)
- [DNS (Domain Name System)](#dns-domain-name-system)
  - [Types of DNS Queries](#types-of-dns-queries)
  - [Making a DNS Query](#making-a-dns-query)
  - [DNS Security Attacks](#dns-security-attacks)
    - [Cache Poisoning](#cache-poisoning)
    - [Denial of Service](#denial-of-service)
    - [Footprinting](#footprinting)
    - [Registration Spoofing](#registration-spoofing)
- [IP protocols and the OSI](#ip-protocols-and-the-osi)
- [UDP (User Diagram Protocol)](#udp-user-diagram-protocol)
- [TCP (Transmission control protocol)](#tcp-transmission-control-protocol)
- [Establishing a TCP connection](#establishing-a-tcp-connection)
- [Closing a TCP connection](#closing-a-tcp-connection)
- [TCP header](#tcp-header)
- [TCP vs UDP](#tcp-vs-udp)
- [FTP (File Transfer Protocol)](#ftp-file-transfer-protocol)
  - [FTP Security issues](#ftp-security-issues)
  - [Active vs passive FTP](#active-vs-passive-ftp)
    - [Implications of ftp connection on firewalls](#implications-of-ftp-connection-on-firewalls)
- [ICMP (Internet Control Message Protocol)](#icmp-internet-control-message-protocol)
  - [ICMP header](#icmp-header)
  - [Ping](#ping)
- [Traceroute](#traceroute)
  - [Unix and Windows Traceroute](#unix-and-windows-traceroute)
- [Common ports](#common-ports)

<!-- /TOC -->

## Types of networks

- LAN - Local area network
  - All users must be trusted
  - Owned by single entity
- MAN - Metropolitan area Network
  - City/town wide network
  - hospitals / corporation offices
- WAN - Wide area network
- Internet
- PAN - Personal area network

## Physical and Logical topologies

### Physical topologies

How network is connected together? via cables or wireless

#### Types of physical topologies

##### Bus topology

- All systems are attached to the same cable segment.
- Rarely used today because of fault tolerance, poor reliability, poor traffic isolation capability and limited scalability.
- It's very hard to secure because all devices can see all the traffic.

##### Ring topology

- Each system has two connections to the network.
- System transmit message from one side, receives from the other one.
- Not secure, messages are going for a full loop until it reaches destination.

#### Star topology

- The most common used topology today.
- All systems are connected to a central device (hub or switch).
- Sender --> Center Point --> Receiver
- __Switched star network__ is the only topology that can prevent other users from eavesdropping on traffic sent between two hosts.

### Logical Topologies

These protocols are responsible for making sure that a signal sent by a system finds its way to it's destination.

There are two general ways systems can communcate on a network:

- Shared segment (Ethernet)
- Allocated time (Token ring)

#### Ethernet

- Layer 2 protocol.
- Only one should be transmitting a frame (chunk of data) at a time.
- __Collisions__ happen when multiple systems are transmitting simultaneously.
- A collision occurs can cause both signals to fail and require systems to retransmit their frames again.
- **CSMA/CD Protocol** (Carrier Sense multiple Access/Collusion Detection)

### Token ring and FDDI

- Not so popular

#### Token ring

![Token Ring](images/Token_ring.svg)

#### FDDI

![](images/FDDI_Dual_Token_Ring.jpg)
![](images/fddi_basic2.gif)

#### Asynchronous Transfer Mode (ATM)

Establishing a channel for each connection allows ATM to provide Quality of Service (QoS). When setting up a virtual circuit, switches along the path can be requested to allocate the desired amount of bandwidth " I need 1MB to support a video conference, Do you have that much available?" If answer is "Yes" then a virtual circuit is created, if the answer is "No" we search for another switch.

- Expensive to set up.
- Not frequently used on LANs.
- Good fit for network that need low-latency traffic such as video streaming.
- Connection-oriented, so before systems can communicate, they must establish a virtual circuit connection between them.
- The virtual circuit is torn down at the end of the connection.

##### Types of ATM

- PVC (Permanent Virtual Circuit)

PVC is set up in advance usually manually.

- SVC (Switched Virtual Circuit)

Is established automatically on the fly

## Wan Technologies

- Point to point communication over a dedicated line.
- high cost.
- Confident as you run solely on the line.

Allowing n sites to directly communicate with each one another would require n+1 links. In such situation it's better to use **Packet-Switched** technology. e.g Frame Relay

### Frame Relay

It's a wan technology similar to Ethernet and Token Ring in that it's based on packet switching.

Lowering the costs of the WAN instead of using dedicated direct links between sites, you will use the Frame Relay Cloud.

### MPLS (Multi-protocol Label Switching)

- Layer 2.5 in OSI model.
- Supports IP traffic including IPv6, VoIP, IP Video.
- Used as a replacement for Frame Relay and ATM.

### ISDN, DSL, Cable Modems

- Connecting throw telephone companies and ISP (Internet service providers)

#### ISDN

- Use "dial-up" connection over phone to connect to ony SPID (Service profile identifier).
- Used mainly as a back up.
- Sometimes can connect with any remote caller, so can be used as a backdoor.

#### DSL (Digital Subscriber Line)

- High-speed network access over traditional telephone lines.
- Operates on regular telephone line with a different modulation frequency, so it can be used in the same time with the telephone service.

#### Cable modems

- Delivered by cable television companies.
- Using DOCSIS (Data Over Cable Interface Specification).

## Network Hardware

### Cabling

![](images/cable_categories.png)
![](images/cable_categories_2.png)

Todays the standard for the modern ethernet networks is to use __CAT 5__ or __CAT 6__ cables

### Network Tap

- Sniff the raw data on a network.
- Needs switch configuration to configure a spanning port.
- Depending on the switch this could have limitations and not gather all the info.

Better option will be a device that operates on the cable level to sniff all the data.

### Vampire Tap

- Works on coaxial cable that uses 10Base5 cabling category.
- It allows you to tap all the traffic without reconfigure the switch.
- Vampire taps allow new connections to be made on a given physical cable while the cable is in use.
- This allows administrators to expand bus-topology network sections without interrupting communications. Without a vampire tap, the cable has to be cut and connectors have to be attached to both ends.

## Network Devices

![](images/network_device.png)

![](images/new_breed_of_swithces.png)

![](images/vlan_nac.png)

## Network design

![](images/network_design.png)

---
---

## OSI MODEL

![](images/osi_model.jpg)

## TCP/IP Model

![](images/osi_vs_tcp_ip.png)
![](images/osi_tcp_models.png)

## How protocol stacks communicate

![](images/how_protocal_stacks_communicate.png)

The basic princible of stack based communication is that: **Data from one layer of the stack can only be understood by the corresponding layer from the remote computer**

This layer independence does have a security implications: for example giving a wrong ip adress for a specific dns service, id IP and DNS layers work together they would probably notice the fake IP, but because they work independently from each other they will not notice that. You need security software to check all the layer and make sure the headers are showing the correct info.

## How TCP packets are created

![](images/how_tcp_packets_are_created.png)
![](images/encapsulation_decapcultations.png)

### IP V4 header

![](images/IP-Header.png)

### IP V6 header

![](images/IP-Header-V6.png)

### IP fragment attacks

- Tiny fragment attack
- Fragment overlap attack
- Sending thousands of initial fragments without sending the rest of the packets could cause IP stack to crash.

## Network Addressing

### Subnet classes

Not used any more as it's a waste of ips. It has been supplanted by CIDR

![](images/subnet_classes.png)

### CIDR (ClassLess Inter-Domain Routing)

- Uses VLSM (Variable Length Subnet Masks) to allocate IPs to subnets according to the individual needs.
- The network/host division can occur at any bit boundary in the address.

![](images/cidr.png)

### Broadcast addresses

![](images/broadcast_addresses.png)

Limited broadcasts are used when computers boot so they can optain DHCP lease or otherwise configure network interfaces.

### Private addresses

![](images/private_addresses.png)
![](images/private_adresses.png)

### IP v6

![](images/ip6_addressing.png)
![](images/ip_v6_addressing.png)
![](images/ip6_features.png)
![](images/ip6_vs_ip4.png)
![](images/ipv6-ipv4-vs-ipv6-header.png)

### MAC and IP address

![](images/mac_ip_1.png)
![](images/mac_ip_2.png)

### ARP (Address Resolution Protocol)

- ARP is a layer 2 broadcast

![](images/arp.png)

## Ports and protocols

![](images/ports_protocols.png)

---

## DNS (Domain Name System)

- static host table:
  - in unix systems: /etc/hosts
  - in windows systems: `%systernroot%\system32\drivers\etc\hosts` with a second similar file in the same directory called `lrnhosts` that contains additional mappings for NetBIOS to lP address translations.

![](images/dns.png)
![](images/dns_hierarchy.png)

### Types of DNS Queries

- Gethostbyname - forward lookup
  - Maps fu lly qualified domain name (FQDN) to IP address
  - e.g. maps www.sans.org to its IP address
- Gethostbyaddr - reverse lookup
  - Maps IP address to FQDN

### Making a DNS Query

```Shell
$ nslookup www.yahoo.com
## Answers that come from cache are referred to as `non-authoritative` answers because a DNS server that does not house the actual database for that domain supplied them.
$ nslookup 216.109.118.72
```

### DNS Security Attacks

![](images/dns_security.png)

#### Cache Poisoning

- DNS cache poisoning attacks involve returning extra data along with the results of a query.
- This extra data contains invalid information, which on vulnerable DNS servers will be written to the DNS cache, thus poisoning the DNS cache for the server.
- The end result is that any traffic for a server with a poisoned entry could be redirected to a server the attacker controls.

##### Defense against Cache Poisoning

- keeping your DNS software updated to the most recent version and keeping patches up-to-date.

#### Denial of Service

- Involve flooding legitimate DNS servers with a large number of queries.
- This effectively makes servers in the domain served by the DNS server unavailable.

#### Footprinting

- Footprinting involves using DNS data to learn about the servers in a network.
- This can be done by requesting
  - zone transfers against improperly configured DNS servers,
  - or by performing reverse DNS lookups against an entire network range.
- The gathered information can be used to formulate attacks against servers in the address space.

##### defense against footprinting

- limit zone transfers to only DNS servers who legitimately require them.
- limit the DNS information available externally to only the information for your internet accessible servers.

#### Registration Spoofing

- Not a real attack, mostly social engineering.
- convincing the domain registrar to use the attacker DNS server.
- Large registrars use their own DNS servers to prevent this attack.

---

## IP protocols and the OSI

![](images/ip_osi.png)

## UDP (User Diagram Protocol)

![](images/udp.png)
![](images/upd_uses.png)

Other important UDP-based protocols include:

- Network Time Protocol (NTP)-Synchronizes time.
- BOOTP/DHCP protocols-Automatically configures network interfaces and load operating systems via the network when they start up.
- Network File System (NFS)-Supports file sharing for Unix-based networks.
- Simple Network Management Protocol (SNMP)-Used as a management tool to query network- and server-based devices for monitoring or troubleshooting purposes.
- Trivial File Transfer Protocol (TFTP)-Used as a method to transfer files from one device to another without requiring authentication. TFTP's most common use is in updating code on network-based devices.

![](images/udp_header_2.png)
![](images/UDP-Header.png)

## TCP (Transmission control protocol)

![](images/tcp.png)

TCP often is a network programmer's protocol of choice. It is probably the easier of the two protocols to program for, because most of the error handling is down inside the transport layer and out of sight from the application code.

![](images/tcp_uses.png)

## Establishing a TCP connection

![](images/tcp_connection.png)

- After a connection is established, the ACK flag is set for every packet. As a result, the presence of the ACK can indicate whether a connection has been established or not.
- In fact, simple packet filters allow all packets with ACK set and assume that they are part of an established connection.
- It is trivial to circumvent such a filter by crafting a packet with the ACK bit set. This technique is often used to probe a network behind a filtering device and called an **ACK scan**.
- To minimize traffic, ACKs are "piggy-backed" (as frequently as possible) onto packets containing data, as opposed to sending a packet with just an ACK.
- The ACKs confirm to the client and server that both ends are still using the connection.

## Closing a TCP connection

![](images/tcp_close_connection.png)

## TCP header

![](images/TCP-Header.png)
![](images/tcp_header_2.png)

## TCP vs UDP

![](images/tcp_vs_udp.png)

## FTP (File Transfer Protocol)

![](images/ftp.png)

### FTP Security issues

- Blind FTP configurations will prevent all or certain users (especially anonymous ones) from being able to list the files or even folders in a directory.
- In order to avoid becoming a warez site, the anonymous user can be permitted to upload into a directory that allows only Put access. ln other words, one anonymous user can upload a file, but another anonymous user will be unable to download the file.
- Another issue to consider with FTP is that all traffic that passes as part of an FTP connection passes in clear text. This means that even with username and password security, an FTP connection or server is only as secure as the network it traverses.
- A potential attacker who has the ability to sniff traffic on a network has the ability to capture username and passwords and even to stealthily obtain files that were transmitted by the FTP server while they were sniffing the network.
- Another common issue with FTP revolves around one specific feature commonly referred to as the `PORT` command. The effect is that a user can cause an FTP server to open a connection from the FTP server directly based upon commands entered through an FTP command/control channel.
- The end result is that a user can effectively bypass firewall controls to port scan a network behind a firewall, where they can connect to an FTP server. They can also obscure their identity by using an FTP server to scan other hosts on the Internet for them.
- In most cases, it is advisable to disable the PORT command entirely to prevent this type of problem.

### Active vs passive FTP

![](images/active_passive_ftp.png)

- An ephemeral port === a port greater than 1023.

#### Implications of ftp connection on firewalls

##### A stateless firewall

that will have no knowledge about the mechanics of the different ports being requested to be opened for FTP. This type of firewall will require the following ports to be opened for FTP to function:

- Active/Passive FTP Command Channel:
  - 21 /TCP permitted inbound to the FTP server from any host coming from an ephemeral port
  - Source port 21/TCP from FTP server permitted outbound to any host on an ephemeral port
- Active FTP Data Channel:
  - Source port 20/tcp from FTP server permitted outbound to any host on an ephemeral port
  - 20/TCP permitted inbound to the FTP server from any host coming from an ephemeral port
- Passive FTP Data Channel:
  - Ephemeral ports to the FTP server permitted inbound from any host on an ephemeral port
  - Ephemeral ports from the FTP server permitted outbound to any host on an ephemeral port

That's a lot of traffic to be permitted through a firewall.

The high traffic essentially provides a mechanism for unauthorized services to be accessible to or from the FTP server that may have nothing to do with FTP at all.

This loose security model can magnify the problems mentioned previously with respect to bounce scans with the `PORT` command and can provide a mechanism for a potentially infected FTP server to have a backdoor installed that is listening on an obscure high port.

If you are stuck with such a firewall, it would be better to disable passive FTP altogether, as active ftp is much less permissive in what it permits through the firewall.

##### A stateful firewall

It would be better, however, to use a stateful firewall that has additional knowledge of the FTP protocol and can dynamically open ports for the data channel based upon reading into command channel packets.

This type of firewall will always permit 21/TCP inbound (and the stateful replies outbound) for valid connections and will prevent the need to leave all of the ephemeral ports wide open at all times, either from 20/TCP or from all ephemeral ports.

## ICMP (Internet Control Message Protocol)

Layer 3 (Network layer) protocol

Purposes:

- To report errors (troubleshooting) rather than transferring information
  - Destination host unreachable
  - Fragmentation needed and OF flag set
- To provide network information
  - Ping - Is the host alive and what's the latency?

### ICMP header

![](images/icmp_header_2.png)
![](images/ICMP-Header.png)

### Ping

![](images/ping.png)

## Traceroute

![](images/traceroute.png)

### Unix and Windows Traceroute

Works differently; might produce different results

- Unix `traceroute` uses UDP packets
- Windows `tracert` uses ICMP packets

Not only is traceroute a great tool for determining paths through the network, but it is also a pretty decent network mapper.

 By carefully examining the output of several runs to different hosts on the same remote network, you can start to notice similarities and differences.

## Common ports

!()[images/common_ports.jpg]
