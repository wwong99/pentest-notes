#!/usr/bin/python

###################################################
#
#   SQLDeli - written by Justin Ohneiser
# ------------------------------------------------
# This program will parse the XML file used to
# power the sqlmap application built into Kali
# Linux and present the contents in an
# interactive menu.
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
VALUE = 'value'
QUERY = 'query'
FILE = '/usr/share/sqlmap/xml/queries.xml'
#
# Designed for use in Kali Linux 4.6.0-kali1-686
###################################################

import os, sys, copy
import xml.etree.ElementTree as ET

# ------------------------------------
# Toolbox
# ------------------------------------

def printLogo():
    os.system("clear")
    print """
 ___ ___| |_____ ___ ___
|_ -| . | |     | .'| . |
|___|_  |_|_|_|_|__,|  _|
      |_|           |_|
          Reference
        """

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

def printHeader(stack):
    s = copy.deepcopy(stack)
    h = "-------"
    while not s.isEmpty():
        if s.peek().get(VALUE):
            h = ("%s: %s\n" % (s.peek().tag, s.peek().get(VALUE))) + h
        elif s.peek().get(QUERY):
            h = ("%s: %s\n" % (s.peek().tag, s.peek().get(QUERY))) + h
        s.pop()
    print h

def printOptions(node):
    index = 0
    for i in node:
        index += 1
        if i.get(VALUE):
            print ("%i:\t%s" % (index, i.get(VALUE)))
        elif i.get(QUERY):
            print ("%s:%s%s" % (i.tag, (2 - int(len(i.tag)/8)) * "\t", i.get(QUERY)))
        else:
            print ("%i:\t%s" % (index, i.tag))

def check(option):
    try:
        return int(option)
    except ValueError:
        return -1

# ------------------------------------
# Retrieve Data
# ------------------------------------

doc = None
try:
    doc = ET.parse(FILE)
except ET.ParseError as e:
    print("[!] Unable to parse XML file: %s\n%s" % (FILE, e))
    sys.exit()
except IOError:
    print("[!] Can't find %s" % FILE)
    sys.exit()

# ------------------------------------
# Process Data
# ------------------------------------

try:
    s=Stack()
    s.push(doc.getroot())
    
    while not s.isEmpty():
        printLogo()
        printHeader(s)
        printOptions(s.peek())
        choice = check(raw_input("\n0:\tBack\n\n>>> "))
        if choice < 0:
            continue
        elif choice == 0:
            s.pop()
        elif choice <= len(s.peek()):
            if s.peek()[choice - 1].get(QUERY):
                continue
            else:
                s.push(s.peek()[choice - 1])
        else:
            continue
except Exception as e:
    print("[!] An error has occurred: %s" % e)
    sys.exit()
except KeyboardInterrupt:
    print("\nExiting")
    sys.exit()

