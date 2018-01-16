# Kali Setup

Once Your Kali VM is Up and Running:

1. Login with the username root and the default password toor

2. Open a Terminal

3. Change Password

    - Always important to change the root password, especially if you enable SSH services.
    - passwd

4. Update Image with the Command:

    - apt-get update
    - apt-get dist-upgrade

5. Setup database for Metasploit

    - This is to configure Metasploit to use a database for stored results and indexing the modules.
    - service postgresql start
    - service Metasploit start

6. *Optional for Metasploit - Enable Logging

    - I keep this as an optional since logs get pretty big, but you have the ability to log every command and result from Metasploit’s Command Line Interface (CLI). This becomes very useful for bulk attack/queries or if your client requires these logs.
    - echo “spool/root/msf_console.log” >/root/.msf4/msfconsole.rc
    - Logs will be stored at/root/msf_console.log

7. Install Discover Scripts (originally called Backtrack-scripts)

    - Discover is used for Passive Enumeration
    - cd/opt/
    - git clone https://github.com/leebaird/discover.git
    - cd discover/
    - ./setup.sh

8. Install Smbexec

    - Smbexec will be used to grab hashes out of the Domain Controller and reverse shells
    - cd/opt/
    - git clone https://github.com/brav0hax/smbexec.git
    - cd smbexec
    - ./install.sh
    - Choose number 1
    - Install to/opt
    - ./install.sh
    - Choose number 4

9. Install Veil

    - Veil will be used to create python based Meterpreter executable
    - cd/opt/
    - git clone https://github.com/veil-evasion/Veil.git
    - cd ./Veil/setup
    - ./setup.sh

10. Download WCE

    - Windows Credential Editor (WCE) will be used to pull passwords from memory
    - cd ~/Desktop
    - wget http://www.ampliasecurity.com/research/wce_v1_41beta_universal.zip
    - unzip -d ./wce wce_v1_41beta_universal.zip

11. Download Mimikatz

    - Mimikatz will be used to pull passwords from memory
    - cd ~/Desktop
    - wget http://blog.gentilkiwi.com/downloads/mimikatz_trunk.zip
    - unzip -d./mimikatz mimikatz_trunk.zip

12. Saving Custom Password Lists

    - Password lists for cracking hashes
    - cd ~/Desktop
    - mkdir ./password_list && cd ./password_list
    - Download large password list via browser and save to ./password_list: https://mega.co.nz/#!3VZiEJ4L!TitrTiiwygI2I_7V2bRWBH6rOqlcJ14tSjss2qR5dqo
    - gzip -d crackstation-human-only.txt.gz
    - wget http://downloads.skullsecurity.org/passwords/rockyou.txt.bz2
    - bzip2 -d rockyou.txt.bz2

13. cd ~/Desktop

14. Download: http://portswigger.net/burp/proxy.html. I would highly recommend you buy the professional version. It is well worth the $300 price tag on it.

15. Setting up Peepingtom

    - Peepingtom will be used to take snapshots of webpages
    - cd/opt/
    - git clone https://bitbucket.org/LaNMaSteR53/peepingtom.git
    - cd ./peepingtom/
    - wget https://gist.github.com/nopslider/5984316/raw/423b02c53d225fe8dfb4e2df9a20bc800cc78e2c/f.
    - wget https://phantomjs.googlecode.com/files/phantomjs1.9.2-linux-i686.tar.bz2
    - tar xvjf phantomjs-1.9.2-linux-i686.tar.bz2
    - cp ./phantomjs-1.9.2-linux-i686/bin/phantomjs .

16. Adding Nmap script

    - The banner-plus.nse will be used for quicker scanning and smarter identification
    - cd/usr/share/nmap/scripts/
    - wget https://raw.github.com/hdm/scan-tools/master/nse/banner-plus.nse

17. Installing PowerSploit

    - PowerSploit are PowerShell scripts for post exploitation
    - cd/opt/
    - git clone https://github.com/mattifestation/PowerSploit.git
    - cd PowerSploit
    - wget https://raw.github.com/obscuresec/random/master/StartListener.py
    - wget https://raw.github.com/darkoperator/powershell_scripts/master/ps_encoder.py

18. Installing Responder

    - Responder will be used to gain NTLM challenge/response hashes
    - cd/opt/
    - git clone https://github.com/SpiderLabs/Responder.git

19. Installing Social Engineering Toolkit (don’t need to re-install on Kali) (SET)

    - SET will be used for the social engineering campaigns
    - cd/opt/
    - git clone https://github.com/trustedsec/social-engineer-toolkit/set/
    - cd set
    - ./setup.py install

20. Install bypassuac

    - Will be used to bypass UAC in the post exploitation sections
    - cd/opt/
    - wget http://www.secmaniac.com/files/bypassuac.zip
    - unzip bypassuac.zip
    - cp bypassuac/bypassuac.rb/opt/metasploit/apps/pro/msf3/scripts/meterpreter/
    - mv bypassuac/uac//opt/metasploit/apps/pro/msf3/data/exploits/

21. Installing BeEF

    - BeEF will be used as an cross-site scripting attack framework
    - apt-get install beef-xss

22. Installing Fuzzing Lists (SecLists)

    - These are scripts to use with Burp to fuzz parameters
    - cd/opt/
    - git clone https://github.com/danielmiessler/SecLists.git

23. Installing Firefox Addons

    - Web Developer Add-on: https://addons.mozilla.org/en-US/firefox/addon/web-developer/
    - Tamper Data: https://addons.mozilla.org/en-US/firefox/addon/tamper-data/
    - Foxy Proxy: https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/
    - User Agent Switcher: https://addons.mozilla.org/en-US/firefox/addon/user-agentswitcher/

