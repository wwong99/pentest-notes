This readme file pertains to the reconscan.py script and all associated scripts. 

Currently these scripts include: 
reconscan.py (main)
dirbust.py  
dnsrecon.py  
ftprecon.py  
reconscan.py  
smbrecon.py  
smtprecon.py  
snmprecon.py  
sshrecon.py

This collection of scripts is intended to be executed remotely against a list of IPs to enumerate discovered 
services such as smb, smtp, snmp, ftp and other.

Author: 
Mike Czumak (T_v3rn1x) -- @SecuritySift

How to use:
reconscan.py is the main script which calls all other scripts. Simply run it and it should do the work for you.
Since I wrote this for a very specific use case I hard-coded all paths so be sure you change them accordingly.
You'll also need to check the directories used for writing and modify accordingly as well. I intentionally kept 
these scripts modular so that each script could also be run on its own.

Warning:
These scripts comes as-is with no promise of functionality or accuracy.  I strictly wrote them for personal use
I have no plans to maintain updates, I did not write them to be efficient and in some cases you may find the 
functions may not produce the desired results so use at your own risk/discretion. I wrote these scripts to 
target machines in a lab environment so please only use them against systems for which you have permission!!  

Modification, Distribution, and Attribution:
You are free to modify and/or distribute this script as you wish.  I only ask that you maintain original
author attribution and not attempt to sell it or incorporate it into any commercial offering (as if it's 
worth anything anyway :)

