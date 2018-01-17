# DNS Enumeration

- NMAP DNS Hostnames Lookup

```ShellSession
nmap -F --dns-server
```

- Host Lookup

```ShellSession
host -t ns [megacorpone.com](http://megacorpone.com/)
```

- Reverse Lookup Brute Force - find domains in the same range

```ShellSession
for ip in $(seq 155 190);do host 50.7.67.$ip;done |grep -v "not found"
```

- Perform DNS IP Lookup

```ShellSession
dig a [domain-name-here.com](http://domain-name-here.com/) @nameserver
```

- Perform MX Record Lookup

```ShellSession
dig mx [domain-name-here.com](http://domain-name-here.com/) @nameserver
```

- Perform Zone Transfer with DIG

```ShellSession
dig axfr [domain-name-here.com](http://domain-name-here.com/) @nameserver
```

## DNS Zone Transfers

- Windows DNS zone transfer

```ShellSession
nslookup -> set type=any -> ls -d [blah.com  ](http://blah.com/)
```

- Linux DNS zone transfer

```ShellSession
dig axfr [blah.com](http://blah.com/) @[ns1.blah.com](http://ns1.blah.com/)
```

- Dnsrecon DNS Brute Force

```ShellSession
dnsrecon -d TARGET -D /usr/share/wordlists/dnsmap.txt -t std --xml ouput.xml
```

- Dnsrecon DNS List of megacorp

```ShellSession
dnsrecon -d [megacorpone.com](http://megacorpone.com/) -t axfr
```

- DNSEnum

```ShellSession
dnsenum zonetransfer.m
```
