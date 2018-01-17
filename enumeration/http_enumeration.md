# HTTP Enumeration

- Search for folders with gobuster:

```ShellSession
gobuster -w /usr/share/wordlists/dirb/common.txt -u $ip
```

- OWasp DirBuster - Http folder enumeration - can take a dictionary file

- Dirb - Directory brute force finding using a dictionary file

```ShellSession
dirb http://$ip/ wordlist.dict

dirb <<http://vm/>>
```

- Dirb against a proxy

```ShellSession
dirb [http://$ip/](http://172.16.0.19/) -p $ip:3129
```

- Nikto

```ShellSession
nikto -h $ip
```

- [HTTP Enumeration](#http-enumeration)

```ShellSession
nmap --script=http-enum -p80 -n $ip/24
```

- Nmap Check the server methods

```ShellSession
nmap --script http-methods --script-args http-methods.url-path='/test' $ip
```

- Get Options available from web server

```ShellSession
  curl -vX OPTIONS vm/test
```

- Uniscan directory finder:

```ShellSession
uniscan -qweds -u <<http://vm/>>
```

- Wfuzz - The web brute forcer

```ShellSession
wfuzz -c -w /usr/share/wfuzz/wordlist/general/megabeast.txt $ip:60080/?FUZZ=test

wfuzz -c --hw 114 -w /usr/share/wfuzz/wordlist/general/megabeast.txt $ip:60080/?page=FUZZ

wfuzz -c -w /usr/share/wfuzz/wordlist/general/common.txt "$ip:60080/?page=mailer&mail=FUZZ"

wfuzz -c -w /usr/share/seclists/Discovery/Web_Content/common.txt --hc 404 $ip/FUZZ
```

- Recurse level 3

```ShellSession
wfuzz -c -w /usr/share/seclists/Discovery/Web_Content/common.txt -R 3 --sc 200 $ip/FUZZ
```

- Open a service using a port knock (Secured with Knockd)

```ShellSession
for x in 7000 8000 9000; do nmap -Pn --host_timeout 201 -max-retries 0 -p $x server_ip_address; done
```

- WordPress Scan - Wordpress security scanner

```ShellSession
wpscan --url $ip/blog --proxy $ip:3129
```

- RSH Enumeration - Unencrypted file transfer system

```ShellSession
auxiliary/scanner/rservices/rsh_login
```

- Finger Enumeration

```ShellSession
finger @$ip

finger batman@$ip
```

- TLS & SSL Testing

```ShellSession
./testssl.sh -e -E -f -p -y -Y -S -P -c -H -U $ip | aha > OUTPUT-FILE.html
```

- Proxy Enumeration (useful for open proxies)

```ShellSession
nikto -useproxy http://$ip:3128 -h $ip
```

- Steganography

```ShellSession
> apt-get install steghide

> steghide extract -sf picture.jpg

> steghide info picture.jpg

> apt-get install stegosuite
```

- The OpenVAS Vulnerability Scanner

```ShellSession
apt-get update

apt-get install openvas

openvas-setup

netstat -tulpn

Login at: https://$ip:939
```
