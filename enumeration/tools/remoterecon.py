#!/usr/bin/python

###################################################
#
#   RemoteRecon - written by Justin Ohneiser
# ------------------------------------------------
# Inspired by reconscan.py by Mike Czumak
#
# This program will conduct full reconnaissance
# on a target using three steps:
#   1. Light NMAP scan -> to identify services
#   2. Modular enumeration for each service
#   3. Heavy NMAP scan
#
# [Warning]:
# This script comes as-is with no promise of functionality or accuracy.  I strictly wrote it for personal use
# I have no plans to maintain updates, I did not write it to be efficient and in some cases you may find the
# functions may not produce the desired results so use at your own risk/discretion. I wrote this script to
# target machines in a lab environment so please only use it against systems for which you have permission!!
#-------------------------------------------------------------------------------------------------------------
# [Modification, Distribution, and Attribution]:
# You are free to modify and/or distribute this script as you wish.  I only ask that you maintain original
# author attribution and not attempt to sell it or incorporate it into any commercial offering (as if it's
# worth anything anyway :)
#
# Designed for use in Kali Linux 4.6.0-kali1-686
###################################################

import os, sys, subprocess, re, urlparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ------------------------------------
#       Toolbox
# ------------------------------------

def printHeader(target):
    print ""
    print "###################################################"
    print "##   Enumerating %s" % target
    print "##"
    print "###################################################"
    print ""

def printUsage():
    print "Usage: %s <target ip>" % sys.argv[0]

def printPlus(message):
    print bcolors.OKGREEN + "[+] " + message + bcolors.ENDC

def printMinus(message):
    print bcolors.WARNING + "[-] " + message + bcolors.ENDC

def printStd(message):
    print "[*] " + message

def printErr(message):
    print bcolors.FAIL + "[!] " + message + bcolors.ENDC

def printDbg(message):
    print bcolors.OKBLUE + "[?] " + message + bcolors.ENDC

def printInBox(command, result):
    top =   "###################################################"
    bot =   "==================================================="
    sub =   "---------------------------------------------------"
    return "%s\n\n%s\n\n%s\n\n%s\n%s\n" % (top, command, sub, result, bot)

def parseNmapScan(results):
    services = {}
    lines = results.split("\n")
    for line in lines:
        ports = []
        line = line.strip()
        if ("tcp" in line or "udp" in line) and ("open" in line) and not ("filtered" in line) and not ("Discovered" in line):
            while "  " in line:
                line = line.replace("  ", " ");
            linesplit = line.split(" ")
            service = linesplit[2]
            port = linesplit[0]
            if service in services:
                ports = services[service]
            ports.append(port)
            services[service] = ports
    return services

def dispatchModules(target, services):
    for service in services:
        ports = services[service]
        if service in KNOWN_SERVICES:
            try:
                KNOWN_SERVICES[service](target, ports)
            except AttributeError:
                printDbg("No module available for %s - %s" % (service, ports))
        else:
            printDbg("No module available for %s - %s" % (service, ports))

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

def parse_ip(s):
    urls = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", s)
    for url in urls:
        url = url.lower()
    return list(set(urls))

def parse_ip_directories(s):
    urls = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+/", s)
    for url in urls:
        url = url.lower()
    return list(set(urls))

# ------------------------------------
#       Setup
# ------------------------------------

def prepareFolder(target):
    printStd("Preparing portfolio")
    directory = "%s/%s" % (os.getcwd(), target)
    if not os.path.exists(directory):
        os.makedirs(directory)
        return None
    return directory

def writeToFile(target, name, content):
    path = "%s/%s/%s.txt" % (os.getcwd(), target, name)
    file = open(path, "a+")
    file.write(content)
    file.close()
    return path

# ------------------------------------
#       Scans
# ------------------------------------

# Light NMAP
# ========================
def conductLightNmap(target):
    printStd("Conducting light nmap scan")
    NAME = "nmap_light"

    # Conduct Scan #
    TCPSCAN = "nmap %s" % target
    UDPSCAN = "nmap -sU -p 161 %s" % target
    tcpResults = ""
    udpResults = ""
    try:
        tcpResults = subprocess.check_output(TCPSCAN, shell=True)
        udpResults = subprocess.check_output(UDPSCAN, shell=True)
        print "%s" % tcpResults

        # Write Results #
        content = "%s" % printInBox(TCPSCAN, tcpResults)
        path = writeToFile(target, NAME, content)
        
        printPlus("Finished light nmap scan: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % TCPSCAN)
    except Exception as e:
        printErr("Unable to conduct light nmap scan:\n\t%s\n\n%s" % (TCPSCAN, e))
        sys.exit(2)

    # Filter Results #
    services = parseNmapScan("%s\n%s" % (tcpResults, udpResults))

    return services
# ========================

# Heavy NMAP
# ========================
def conductHeavyNmap(target):
    printStd("Conducting heavy nmap scan")
    NAME = "nmap_heavy"
    
    # Conduct Heavy nmap Scan #
    TCPSCAN = "nmap -A --top-ports 10000 %s" % target
    try:
        tcpResults = subprocess.check_output(TCPSCAN, shell=True)
        
        # Write Results #
        content = "%s" % printInBox(TCPSCAN, tcpResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished heavy nmap scan: %s/%s/nmap_heavy.txt" % (os.getcwd(), target))
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % TCPSCAN)
    except Exception:
        printErr("Unable to conduct heavy nmap scan:\n\t%s" % TCPSCAN)

    printStd("Conducting UDP scan")

    # Conduct UDP Scan #
    UDPSCAN = "nmap -sU --top-ports 100 %s" % target
    try:
        udpResults = subprocess.check_output(UDPSCAN, shell=True)
        
        # Write Results #
        content = "%s" % printInBox(UDPSCAN, udpResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished UDP scan: %s/%s/nmap_heavy.txt" % (os.getcwd(), target))
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % UDPSCAN)
    except Exception:
        printErr("Unable to conduct UDP scan:\n\t%s" % UDPSCAN)
# ========================

# FTP
# ========================
def ftp(target, ports):
    printStd("Investigating FTP")
    NAME = "ftp"
    
    # Conduct nmap Scan #
    portString = ""
    for port in ports:
        port = port.split("/")[0]
        portString += "%s," % port
    SCRIPTS = "ftp-vuln-*, ftp-anon"
    NMAPSCAN = "nmap -p %s -sV -sC --script=\"%s\" %s" % (portString, SCRIPTS, target)
    try:
        nmapResults = subprocess.check_output(NMAPSCAN, shell=True)

        # Write Results #
        content = "%s" % printInBox(NMAPSCAN, nmapResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished investigating FTP: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % NMAPSCAN)
    except Exception:
        printErr("Unable to conduct FTP scan:\n\t%s" % NMAPSCAN)
# ========================

# SMTP
# ========================
def smtp(target, ports):
    printStd("Investigating SMTP")
    NAME = "smtp"

    # Conduct nmap Scan #
    portString = ""
    for port in ports:
        port = port.split("/")[0]
        portString += "%s," % port
    NMAPSCAN = "nmap -p %s -sV --script=\"smtp-vuln*\" %s" % (portString, target)
    try:
        nmapscanResults = subprocess.check_output(NMAPSCAN, shell=True)

        # Write Results #
        content = "%s" % printInBox(NMAPSCAN, nmapscanResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished scanning SMTP: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % NMAPSCAN)
    except Exception:
        printErr("Unable to conduct SMTP scan:\n\t%s" % NMAPSCAN)

    # Conduct Brute #
    printStd("Trying to brute-force SMTP users")
    SCAN1 = "smtp-user-enum -M EXPN -U /usr/share/fern-wifi-cracker/extras/wordlists/common.txt -t %s" % target
    try:
        scan1Results = subprocess.check_output(SCAN1, shell=True)
        
        # Write Results #
        content = "%s" % (printInBox(SCAN1, scan1Results))
        path = writeToFile(target, NAME, content)
        printPlus("Finished investigating SMTP: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % SCAN1)
    except Exception:
        printErr("Unable to conduct SMTP brute force:\n\t%s\n\t%s" % SCAN1)
# ========================

# POP3
# ========================
def pop3(target, ports):
    printStd("Investigating POP3")
    NAME = "pop3"
    
    # Conduct Basic Scan"
    portString = ""
    for port in ports:
        port = port.split("/")[0]
        portString += "%s," % port
    NMAPSCAN = "nmap -p %s -sV --script=\"pop3-capabilities,pop3-ntlm-info\" %s" % (portString, target)
    try:
        nmapscanResults = subprocess.check_output(NMAPSCAN, shell=True)

        # Write Results #
        content = "%s" % printInBox(NMAPSCAN, nmapscanResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished enumerating POP3: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % NMAPSCAN)
    except Exception:
        printErr("Unable to enumerate POP3:\n\t%s" % NMAPSCAN)

    # Conduct Brute Force"
    printStd("Trying to brute-force POP3 users")
    BRUTE = "nmap -p %s --script=\"pop3-brute\" %s" % (portString, target)
    try:
        bruteResults = subprocess.check_output(BRUTE, shell=True)

        # Write Results #
        content = "%s" % printInBox(BRUTE, bruteResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished investigating POP3: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % BRUTE)
    except Exception:
        printErr("Unable to brute-force POP3 users:\n\t%s" % BRUTE)
# ========================

# IMAP
# ========================
def imap(target, ports):
    printStd("Investigating IMAP")
    NAME = "imap"
    
    # Conduct Basic Scan"
    portString = ""
    for port in ports:
        port = port.split("/")[0]
        portString += "%s," % port
    NMAPSCAN = "nmap -p %s -sV --script=\"imap-capabilities,imap-ntlm-info\" %s" % (portString, target)
    try:
        nmapscanResults = subprocess.check_output(NMAPSCAN, shell=True)
        
        # Write Results #
        content = "%s" % printInBox(NMAPSCAN, nmapscanResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished enumerating IMAP: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % NMAPSCAN)
    except Exception:
        printErr("Unable to enumerate IMAP:\n\t%s" % NMAPSCAN)

    # Conduct Brute Force"
    printStd("Trying to brute-force IMAP users")
    BRUTE = "nmap -p %s --script=\"imap-brute\" %s" % (portString, target)
    try:
        bruteResults = subprocess.check_output(BRUTE, shell=True)
        
        # Write Results #
        content = "%s" % printInBox(BRUTE, bruteResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished investigating IMAP: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % BRUTE)
    except Exception:
        printErr("Unable to brute-force IMAP users:\n\t%s" % BRUTE)
# ========================

# SMB
# ========================
def smb(target, ports):
    printStd("Investigating SMB")
    NAME = "smb"

    # Conduct Vulnerability Scans #
    SCAN1 = "nmap -sV -sC --script=\"smb-vuln-*,samba-vuln-*\" -p 445,139 %s" % target
    SCAN2 = "nmap -sU -sV -sC --script=\"smb-vuln-*\" -p U:137,T:139 %s" % target
    try:
        scan1Results = subprocess.check_output(SCAN1, shell=True)
        scan2Results = subprocess.check_output(SCAN2, shell=True)

        # Write Results #
        content = "%s\n%s" % (printInBox(SCAN1, scan1Results), printInBox(SCAN2, scan2Results))
        path = writeToFile(target, NAME, content)
        printPlus("Finished investigating SMB Vulnerabilities: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s\n\t%s" % (SCAN1, SCAN2))
    except Exception:
        printErr("Unable to conduct SMB vulnerability scan:\n\t%s\n\t%s" % (SCAN1, SCAN2))

    # Conduct Scan #
    printStd("Investigating SMB Access")
    LOOKUP = "nmblookup -A %s" % target
    SCAN = "enum4linux %s" % target
    ADVICE = "use :: smbclient //<server>/<share> -I <target ip> -N :: to mount shared drive anonymously"
    try:
        # Lookup #
        lookupResults = subprocess.check_output(LOOKUP, shell=True)

        # Write Results #
        content = "%s" % printInBox(LOOKUP, lookupResults)
        path = writeToFile(target, NAME, content)
        
        # Scan #
        scanResults = subprocess.check_output(SCAN, shell=True)

        # Write Results #
        content = "%s" % printInBox(SCAN, "%s\n\n%s" % (scanResults, ADVICE))
        path = writeToFile(target, NAME, content)
        printPlus("Finished investigating SMB: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % SCAN)
    except Exception:
        printErr("Unable to conduct SMB scan:\n\t%s" % SCAN)
# ========================

# HTTP
# ========================
def http(target, ports):
    printStd("Investigating HTTP")
    NAME = "http"

    # Conduct nmap Scan #
    SCRIPTS = "http-methods,http-robots.txt,http-vuln-*,http-userdir-enum,http-iis-webdav-vuln,http-majordomo2-dir-traversal,http-axis2-dir-traversal,http-tplink-dir-traversal,http-useragent-tester"
    
    portString = ""
    for port in ports:
        port = port.split("/")[0]
        portString += "%s," % port
    NMAPSCAN = "nmap -p %s -sC -sV --script=\"%s\" %s" % (portString, SCRIPTS, target)
    try:
        nmapscanResults = subprocess.check_output(NMAPSCAN, shell=True)

        # Write Results #
        content = "%s" % printInBox(NMAPSCAN, nmapscanResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished scanning HTTP: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % NMAPSCAN)
    except Exception:
        printErr("Unable to conduct HTTP scan:\n\t%s" % NMAPSCAN)

    # Conduct WebDav Scan #
    printStd("Trying to identify WebDav")
    WEBDAVSCAN = "nmap -p %s --script http-webdav-scan %s -d 2>/dev/null | grep 'http-webdav-scan %s'" % (portString, target, target)
    try:
        webdavscanResults = subprocess.check_output(WEBDAVSCAN, shell=True)

        # Write Results #
        content = "%s" % printInBox(WEBDAVSCAN, webdavscanResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished scanning WebDav: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % WEBDAVSCAN)
    except subprocess.CalledProcessError as ex:
        if ex.returncode != 1:
            raise Exception
    except Exception:
        printErr("Unable to perform WebDav analysis:\n\t%s" % WEBDAVSCAN)

    # Conduct Brute #
    for port in ports:
        urlArr = []
        urlDir = ["/"]
        port = port.split("/")[0]
        printStd("Trying to brute-force HTTP directories on port %s" % port)
        DIRB = "dirb http://%s:%s /usr/share/wordlists/dirb/common.txt -S -r" % (target, port)
        try:
            dirbResults = subprocess.check_output(DIRB, shell=True)

            # Parse Results for Spider #
            urlArr = parse_ip(dirbResults)
            urlDir = parse_ip_directories(dirbResults)
            
            # Write Results #
            content = "%s" % printInBox(DIRB, dirbResults)
            path = writeToFile(target, NAME, content)
            printPlus("Finished HTTP brute-force against port %s: %s - Found: %s" % (port, path, len(urlArr)))
        except KeyboardInterrupt:
            printMinus("Skipping:\n\t%s" % DIRB)
        except Exception:
            printErr("Unable to brute-force HTTP on port %s:\n\t%s" % (port, DIRB))

        # Conduct Spider #
        SCRIPTS = "http-shellshock,http-auth-finder,http-backup-finder,http-comments-displayer,http-config-backup,http-default-accounts,http-dombased-xss,http-errors,http-fileupload-exploiter,http-method-tamper,http-passwd,http-phpmyadmin-dir-traversal,http-phpself-xss,http-rfi-spider,http-sitemap-generator,http-sql-injection,http-stored-xss,http-unsafe-output-escaping"

        # Spidered Vulnerability Scans
        for url in urlDir:
            # Nikto Scan #
            NIKTO = "nikto -host http://%s:%s -root %s" % (target, port, urlparse.urlparse(url).path)
            try:
                printStd("Crawling %s for vulnerabilities (nikto)" % url)
            
                niktoResults = subprocess.check_output(NIKTO, shell=True)
                # ...sometimes this doesn't work...?
                if "0 host(s) tested" in niktoResults:
                    niktoResults = subprocess.check_output(NIKTO, shell=True)
            
                if "0 host(s) tested" in niktoResults:
                    printDbg(niktoResults)
                    raise Exception
            
                # Write Results #
                content = "%s" % printInBox(NIKTO, niktoResults)
                path = writeToFile(target, NAME, content)
                printPlus("Finished crawling %s for vulnerabilities (nikto): %s" % (url, path))
            
            except KeyboardInterrupt:
                printMinus("Skipping:\n\t%s" % NIKTO)
            except Exception as e:
                print str(e)
                printErr("Unable to conduct HTTP vulnerability crawl (nikto):\n\t%s" % NIKTO)

            # Nmap Scan #
            SCRIPTARGS = "http-shellshock.uri=%(url)s,http-backup-finder.url=%(url)s,http-config-backup.path=%(url)s,http-default-accounts.category=web,http-default-accounts.basepath=%(url)s,httpspider.url=%(url)s,http-method-tamper.uri=%(url)s,http-passwd.root=%(url)s,http-phpmyadmin-dir-traversal.dir=%(url)s,http-phpself-xss.uri=%(url)s,http-rfi-spider.url=%(url)s,http-sitemap-generator.url=%(url)s,http-sql-injection.url=%(url)s,http-unsafe-output-escaping.url=%(url)s" % {"url":urlparse.urlparse(url).path}
            VULNSCAN = "nmap -p %s %s --script=\"%s\" --script-args=\"%s\" 2>&1" % (port, target, SCRIPTS, SCRIPTARGS)
            try:
                printStd("Crawling %s for vulnerabilities (nmap)" % url)
                vulnscanResults = subprocess.check_output(VULNSCAN, shell=True)

                # Write Results #
                content = "%s" % printInBox(VULNSCAN, vulnscanResults)
                path = writeToFile(target, NAME, content)
                printPlus("Finished crawling %s for vulnerabilities (nmap): %s" % (url, path))

            except KeyboardInterrupt:
                printMinus("Skipping:\n\t%s" % VULNSCAN)
            except Exception:
                printErr("Unable to conduct HTTP vulnerability crawl (nmap):\n\t%s" % VULNSCAN)

# ========================

# HTTPS
# ========================
def https(target, ports):
    printStd("Investigating HTTPS")
    NAME = "https"
    
    # Conduct NMAP Scan #
    SCRIPTS = "http-methods,http-robots.txt,http-vuln-*,http-shellshock,http-userdir-enum,http-iis-webdav-vuln,http-majordomo2-dir-traversal,http-axis2-dir-traversal,http-tplink-dir-traversal,http-useragent-tester,ssl-*"

    portString = ""
    for port in ports:
        port = port.split("/")[0]
        portString += "%s," % port
    NMAPSCAN = "nmap -p %s -sV -sC --script=\"%s\" %s" % (portString, SCRIPTS, target)
    try:
        nmapscanResults = subprocess.check_output(NMAPSCAN, shell=True)

        # Write Scan Results #
        content = "%s" % printInBox(NMAPSCAN, nmapscanResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished scanning HTTPS: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % NMAPSCAN)
    except Exception:
        printErr("Unable to conduct HTTPS scan:\n\t%s" % NMAPSCAN)

    # Conduct WebDav Scan #
    printStd("Trying to identify WebDav")
    WEBDAVSCAN = "nmap -p %s --script http-webdav-scan %s -d 2>/dev/null | grep 'http-webdav-scan %s'" % (portString, target, target)
    try:
        webdavscanResults = subprocess.check_output(WEBDAVSCAN, shell=True)
        
        # Write Results #
        content = "%s" % printInBox(WEBDAVSCAN, webdavscanResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished scanning WebDav: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % WEBDAVSCAN)
    except subprocess.CalledProcessError as ex:
        if ex.returncode != 1:
            raise Exception
    except Exception:
        printErr("Unable to perform WebDav analysis:\n\t%s" % WEBDAVSCAN)

    # Conduct Brute #
    for port in ports:
        urlArr = []
        urlDir = ["/"]
        port = port.split("/")[0]
        printStd("Trying to brute-force HTTPS directories on port %s" % port)
        DIRB = "dirb https://%s:%s /usr/share/wordlists/dirb/common.txt -S -r" % (target, port)
        try:
            dirbResults = subprocess.check_output(DIRB, shell=True)
            
            # Parse Results for Spider #
            urlArr = parse_ip(dirbResults)
            urlDir = parse_ip_directories(dirbResults)
            
            # Write Results #
            content = "%s" % printInBox(DIRB, dirbResults)
            path = writeToFile(target, NAME, content)
            printPlus("Finished HTTPS brute-force against port %s: %s - Found: %s" % (port, path, len(urlArr)))
        except KeyboardInterrupt:
            printMinus("Skipping:\n\t%s" % DIRB)
        except Exception:
            printErr("Unable to brute-force HTTPS on port %s:\n\t%s" % (port, DIRB))
        
        # Conduct Spider #
        SCRIPTS = "http-auth-finder,http-backup-finder,http-comments-displayer,http-config-backup,http-default-accounts,http-dombased-xss,http-errors,http-fileupload-exploiter,http-method-tamper,http-passwd,http-phpmyadmin-dir-traversal,http-phpself-xss,http-rfi-spider,http-sitemap-generator,http-sql-injection,http-stored-xss,http-unsafe-output-escaping"

        # Spidered Vulnerability Scans
        for url in urlDir:
            # Nikto Scan #
            NIKTO = "nikto -host https://%s:%s -root %s -ssl" % (target, port, urlparse.urlparse(url).path)
            try:
                printStd("Crawling %s for vulnerabilities (nikto)" % url)
                
                niktoResults = subprocess.check_output(NIKTO, shell=True)
                # ...sometimes this doesn't work...?
                if "0 host(s) tested" in niktoResults:
                    niktoResults = subprocess.check_output(NIKTO, shell=True)
                
                if "0 host(s) tested" in niktoResults:
                    raise Exception
                
                # Write Results #
                content = "%s" % printInBox(NIKTO, niktoResults)
                path = writeToFile(target, NAME, content)
                printPlus("Finished crawling %s for vulnerabilities (nikto): %s" % (url, path))
            
            except KeyboardInterrupt:
                printMinus("Skipping:\n\t%s" % NIKTO)
            except Exception:
                printErr("Unable to conduct HTTPS vulnerability crawl (nikto):\n\t%s" % NIKTO)
            
            # Nmap Scan #
            SCRIPTARGS = "http-backup-finder.url=%(url)s,http-config-backup.path=%(url)s,http-default-accounts.category=web,http-default-accounts.basepath=%(url)s,httpspider.url=%(url)s,http-method-tamper.uri=%(url)s,http-passwd.root=%(url)s,http-phpmyadmin-dir-traversal.dir=%(url)s,http-phpself-xss.uri=%(url)s,http-rfi-spider.url=%(url)s,http-sitemap-generator.url=%(url)s,http-sql-injection.url=%(url)s,http-unsafe-output-escaping.url=%(url)s" % {"url":urlparse.urlparse(url).path}
            VULNSCAN = "nmap -p %s %s --script=\"%s\" --script-args=\"%s\" 2>&1" % (port, target, SCRIPTS, SCRIPTARGS)
            try:
                printStd("Crawling %s for vulnerabilities (nmap)" % url)
                vulnscanResults = subprocess.check_output(VULNSCAN, shell=True)
                
                # Write Results #
                content = "%s" % printInBox(VULNSCAN, vulnscanResults)
                path = writeToFile(target, NAME, content)
                printPlus("Finished crawling %s for vulnerabilities (nmap): %s" % (url, path))

            except KeyboardInterrupt:
                printMinus("Skipping:\n\t%s" % VULNSCAN)
            except Exception:
                printErr("Unable to conduct HTTPS vulnerability crawl (nmap):\n\t%s" % VULNSCAN)
# ========================

# SNMP
# ========================
def snmp(target, ports):
    printStd("Investigating SNMP")
    NAME = "snmp"

    # Conduct Scans #
    portString = ""
    for port in ports:
        port = port.split("/")[0]
        portString += "%s," % port
    NMAPSCAN = "nmap -sU -p %s --script=\"snmp-*\" %s" % (portString, target)

    ONESIXTYONE = "onesixtyone -c /usr/share/doc/onesixtyone/dict.txt %s 2>&1" % target
    ADVICE = "If match community string, use :: snmpwalk -c <community string> -v1 %s :: to enumerate" % target
    foundCount = 0
    try:
        nmapscanResults = subprocess.check_output(NMAPSCAN, shell=True)

        # Write Results #
        content = "%s" % printInBox(NMAPSCAN, nmapscanResults)
        path = writeToFile(target, NAME, content)
        
        onesixtyoneResults = subprocess.check_output(ONESIXTYONE, shell=True)
        foundCount = len(onesixtyoneResults.split('\n')) - 1
        
        # Write Results #
        content = "%s" % printInBox(ONESIXTYONE, onesixtyoneResults)
        path = writeToFile(target, NAME, content)
        
        printPlus("Finished investigating SNMP: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % ONESIXTYONE)
    except Exception:
        printErr("Unable to conduct SNMP scan:\n\t%s" % ONESIXTYONE)

    if foundCount > 1:
        printStd("Mapping SNMP")
        WALK = "for s in $(onesixtyone -c /usr/share/doc/onesixtyone/dict.txt %s | grep %s | cut -d ' ' -f 2 | sed -e 's/\[//g' -e 's/\]//g');do snmpwalk -c $s -v1 %s;done" % (target, target, target)
        try:
            walkResults = subprocess.check_output(WALK, shell=True)

            # Write Results #
            content = "%s" % printInBox(WALK, walkResults)
            path = writeToFile(target, NAME, content)

            printPlus("Finished mapping SNMP: %s" % path)
        except KeyboardInterrupt:
            printMinus("Skipping:\n\t%s" % WALK)
        except Exception:
            printErr("unable to map SNMP:\n\t%s" % WALK)
# ========================

# MS-SQL
# ========================
def ms_sql(target, ports):
    printStd("Investigating MS-SQL")
    NAME = "ms_sql"

    # Conduct nmap Scan #
    portString = ""
    for port in ports:
        port = port.split("/")[0]
        portString += "%s," % port
    NMAPSCAN = "nmap -p %s -sV -sC %s" % (portString, target)
    try:
        nmapscanResults = subprocess.check_output(NMAPSCAN, shell=True)

        # Write Scan Results #
        content = "%s" % printInBox(NMAPSCAN, nmapscanResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished scanning MS-SQL: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % NMAPSCAN)
    except Exception:
        printErr("Unable to conduct MS-SQL scan:\n\t%s" % NMAPSCAN)

    # Conduct Brute #
    printStd("Trying to brute-force MS-SQL")
    BRUTE = "medusa -h %s -U /usr/share/wordlists/metasploit/default_users_for_services_unhash.txt -P /usr/share/wordlists/metasploit/default_pass_for_services_unhash.txt -M mssql -L -f 2>&1" % (target)
    try:
        bruteResults = subprocess.check_output(BRUTE, shell=True)

        # Write Brute Results #
        content = "%s" % printInBox(BRUTE, bruteResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished conducting MS-SQL brute-force: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % BRUTE)
    except Exception:
        printErr("Unable to conduct MS-SQL brute-force:\n\t%s" % BRUTE)
# ========================

# MySQL
# ========================
def mysql(target, ports):
    printStd("Investigating MySQL")
    NAME = "mysql"
    
    # Conduct nmap Scan #
    portString = ""
    for port in ports:
        port = port.split("/")[0]
        portString += "%s," % port
    NMAPSCAN = "nmap -p %s -sV -sC %s" % (portString, target)
    try:
        nmapscanResults = subprocess.check_output(NMAPSCAN, shell=True)

        # Write Scan Results #
        content = "%s" % printInBox(NMAPSCAN, nmapscanResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished scanning MySQL: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % NMAPSCAN)
    except Exception:
        printMinus("Unable to conduct MySQL scan:\n\t%s" % NMAPSCAN)

    # Conduct Brute #
    printStd("Trying to brute-force MySQL")
    BRUTE = "medusa -h %s -U /usr/share/wordlists/metasploit/default_users_for_services_unhash.txt -P /usr/share/wordlists/metasploit/default_pass_for_services_unhash.txt -M mysql -L -f 2>&1" % (target)
    try:
        bruteResults = subprocess.check_output(BRUTE, shell=True)

        # Write Brute Results #
        content = "%s" % printInBox(BRUTE, bruteResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished conducting MySQL brute-force: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % BRUTE)
    except Exception:
        printErr("Unable to conudct MySQL brute-foce:\n\t%s" % BRUTE)
# ========================
# NFS
# ========================
def nfs(target, ports):
    printStd("Investigating NFS")
    NAME = "nfs"
    
    # Conduct rpcinfo #
    RPCINFO = "rpcinfo -s %s" % target
    try:
        rpcinfoResults = subprocess.check_output(RPCINFO, shell=True)
    
        # Write Results #
        content = "%s" % printInBox(RPCINFO, rpcinfoResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished scanning RPC processes: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % RPCINFO)
    except Exception:
        printErr("Unable to scan RPC processes:\n\t%s" % RPCINFO)
    
    # Conduct showmount #
    printStd("Capturing accessible NFS shares")
    SHOWMOUNT = "showmount -e %s" % target
    ADVICE = "Use :: mount -t ntf %s:[share] /mnt/%s -o nolock :: to mount share"
    try:
        showmountResults = subprocess.check_output(SHOWMOUNT, shell=True)
    
        # Write Results #
        content = "%s" % printInBox(SHOWMOUNT, "%s\n\n%s" % (showmountResults, ADVICE))
        path = writeToFile(target, NAME, content)
        printPlus("Captured accessible NFS shares: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % SHOWMOUNT)
    except Exception:
        printErr("Unable to capture accessible NFS shares:\n\t%s" % SHOWMOUNT)
    
    # Conduct nmap Scan #
    printStd("Exploring accessible NFS shares")
    portString = ""
    for port in ports:
        port = port.split("/")[0]
        portString += "%s," % port
    NMAPSCAN = "nmap -p %s -sV -sC --script=\"nfs-showmount,nfs-ls\" %s" % (portString, target)
    try:
        nmapResults = subprocess.check_output(NMAPSCAN, shell=True)
        
        # Write Results #
        content = "%s" % printInBox(NMAPSCAN, nmapResults)
        path = writeToFile(target, NAME, content)
        printPlus("Finished investigating NFS: %s" % path)
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % NMAPSCAN)
    except Exception:
        printErr("Unable to conduct NFS scan:\n\t%s" % NMAPSCAN)
# ========================

# ------------------------------------
#       Main
# ------------------------------------

KNOWN_SERVICES = {
    "ftp"           :   ftp,
    "smtp"          :   smtp,
    "pop3"          :   pop3,
    "imap"          :   imap,
    "netbios-ssn"   :   smb,
    "http"          :   http,
    "http-alt"      :   http,
    "http-proxy"    :   http,
    "https"         :   https,
    "snmp"          :   snmp,
    "ms-sql-s"      :   ms_sql,
    "mysql"         :   mysql,
    "rpcbind"       :   nfs
}

def main(argv):
    if len(sys.argv) != 2:
        printUsage()
        sys.exit(2)
    
    TARGET = sys.argv[1]
    if not validate_ip(TARGET):
        printMinus("Invalid IP Address")
        printUsage()
        sys.exit(2)

    printHeader(TARGET)
    error = prepareFolder(TARGET)
    if None != error:
        printMinus("Portfolio for %s already exists at %s" % (TARGET, error))
        printUsage()
        sys.exit(2)

    try:
        SERVICES = conductLightNmap(TARGET)
        dispatchModules(TARGET, SERVICES)
        conductHeavyNmap(TARGET)
    except KeyboardInterrupt:
        print "\n\nExiting.\n"
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
