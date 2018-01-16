#!/bin/bash
# linuxenum-btr.sh > privesc-enum.txt seklinde kullanalim
# SCRIPTI /var/tmp DIZINI ALTINDA CALISTIRALIM
# EGER SCRIPTI KULLANICINIZIN HOME DIZINI ALTINDA CALISTIRIRSANIZ KENDINIZE
printf '\n======================================================='
printf '\nTEMEL BILGILER'
printf '\n======================================================='
printf '\n*******************************************************\n'
printf 'KULLANICI ADI - whoami'
printf '\n*******************************************************\n'
whoami 2>/dev/null
printf '\n*******************************************************\n'
printf 'KULLANICI ID SI VE GRUPLARI - id'
printf '\n*******************************************************\n'
id 2>/dev/null
printf '\n*******************************************************\n'
printf 'HOME DIZINIMIZ - echo $HOME'
printf '\n*******************************************************\n'
echo $HOME 2>/dev/null
printf '\n*******************************************************\n'
printf 'HOME DIZIN ICERIGIMIZ VE ERISIM HAKLARI - ls -ahl ~'
printf '\n*******************************************************\n'
ls -ahl ~ 2>/dev/null
printf '\n*******************************************************\n'
printf 'SUDO HAKLARIMIZ - sudo -l -n shell escape imkani verebilecek
komutlara ozellikle dikkat'
printf '\nCikti içinde !env_reset komutu varsa ve sudo versiyonu uygunsa
cevresel degiskenler vasitasiyla priv esc yapilabilir'
printf '\nsudo privilege escalation metodları:
https://www.securusglobal.com/community/2014/03/17/how-i-got-root-with-sudo/'
printf '\nsudo -l -n komutu ile parola vermeden sudo haklarimizi listelemeye
calisiyoruz'
printf '\nEger sudo -l komutu icin parola verilmesi gerekiyorsa ve biz
baglantimizi parolasini bildigimiz bir kullanici ile gerceklestirmis isek bu
komutu manuel olarak calistirmayi unutmayalim'
printf '\n*******************************************************\n'
sudo -l -n 2>/dev/null | tee sudo-config-enum.txt
printf '\n*******************************************************\n'
printf 'SHELL ESCAPE IMKANI VEREN SUDO HAKLARIMIZ - grep komutu ilgisiz
satirlari da yakalayabiliyor o yuzden scripti okuyunuz - tcpdump makalesi
https://www.stevencampbell.info/2016/04/why-sudo-tcpdump-is-dangerous/'
printf '\n*******************************************************\n'
cat sudo-config-enum.txt 2>/dev/null | grep -i -E 'vi|awk|perl|find|nmap|man|more|less|tcpdump|bash|sh|vim|nc|netcat|python|ruby|lua|irb'
printf '\n*******************************************************\n'
printf 'SUDO VERSIYONU - sudo -V: sudo - sudoedit ile ilgili acikliklari
kullanabiliriz 1.8.14 versiyonu icin bakiniz https://www.exploitdb.com/exploits/37710/
1.6.9p21 / 1.7.2p4 için bakiniz https://www.exploitdb.com/exploits/11651/
digerleri icin mutlaka google dan arama yapiniz'
printf '\n*******************************************************\n'
sudo -V
printf '\n*******************************************************\n'
printf 'REDHAT ICIN SUDO PAKETI VERSIYONU'
printf '\n*******************************************************\n'
rpm -q sudo 2>/dev/null
printf '\n*******************************************************\n'
printf 'SUDOERS DOSYASI ERISIM HAKLARI'
printf '\n*******************************************************\n'
ls -al /etc/sudoers 2>/dev/null
printf '\n*******************************************************\n'
printf 'SUDOERS DOSYASI ICERIGI- GOREBILIYORSAK - cat /etc/sudoers'
printf '\n*******************************************************\n'
cat /etc/sudoers 2>/dev/null
printf '\n*******************************************************\n'
printf 'SISTEM BILGISI - uname -a'
printf '\n*******************************************************\n'
uname -a 2>/dev/null
printf '\n*******************************************************\n'
printf 'KERNEL BILGISI - cat /proc/version'
printf '\n*******************************************************\n'
cat /proc/version 2>/dev/null
printf '\n*******************************************************\n'
printf 'ISLEMCI MIMARI BILGISI - lscpu'
printf '\n*******************************************************\n'
lscpu 2>/dev/null
printf '\n*******************************************************\n'
printf 'ISLETIM SISTEMI BILGISI'
printf '\n*******************************************************\n'
cat /etc/*-release
printf '\n*******************************************************\n'
printf 'SUNUCU ADI - hostname'
printf '\n*******************************************************\n'
hostname 2>/dev/null
printf '\n*******************************************************\n'
printf 'ROOT - YANI ID SI 0 OLAN - KULLANICILARIN LISTESI'
printf '\n*******************************************************\n'
grep -v -E '^#' /etc/passwd | awk -F: '$3 == 0{print $1}'
printf '\n*******************************************************\n'
printf 'SUDO GRUBUNA UYE KULLANICILAR'
printf '\n*******************************************************\n'
for i in $(cat /etc/passwd 2>/dev/null| cut -d':' -f1 2>/dev/null);do id $i;done 2>/dev/null | grep -i "sudo"
printf '\n*******************************************************\n'
printf 'PASSWD DOSYASI - cat /etc/passwd'
printf '\n*******************************************************\n'
cat /etc/passwd 2>/dev/null
printf '\n*******************************************************\n'
printf 'FREEBSD ICIN PASSWD DOSYASI - cat /etc/master.passwd'
printf '\n*******************************************************\n'
cat /etc/master.passwd 2>/dev/null
printf '\n*******************************************************\n'
printf 'KULLANICILARIN GRUP UYELIKLERI - groups bolumune bakiniz'
printf '\n*******************************************************\n'
for i in $(cat /etc/passwd 2>/dev/null| cut -d':' -f1 2>/dev/null);do id $i;done 2>/dev/null
printf '\n*******************************************************\n'
printf 'KULLANICI LISTESI - SHELL UYGULAMASINA GORE SIRALI - cat /etc/passwd
| awk -F: {print $7\011$1} | sort'
printf '\n*******************************************************\n'
cat /etc/passwd | awk -F':' '{print $7"\011"$1}' | sort
printf '\n*******************************************************\n'
printf 'KULLANICI LISTESI - HOME DIZININE GORE SIRALI - cat /etc/passwd | awk
-F: {print $6\011$1} | sort'
printf '\n*******************************************************\n'
cat /etc/passwd | awk -F':' '{print $6"\011"$1}' | sort
printf '\n*******************************************************\n'
printf 'DAHA ONCE LOGON OLMUS KULLANICILAR - HER ZAMAN SAGLIKLI BILGI VERMEYEBILIR - lastlog | grep -v Never'
printf '\n*******************************************************\n'
lastlog | grep -v "Never" 2>/dev/null
printf '\n*******************************************************\n'
printf 'SON KULLANICI AKTIVITELERI - last'
printf '\n*******************************************************\n'
last 2>/dev/null
printf '\n*******************************************************\n'
printf 'GROUP DOSYASI - cat /etc/group - ozellikle sudo grup uyeliklerine
dikkat edelim'
printf '\n*******************************************************\n'
cat /etc/group 2>/dev/null
printf '\n*******************************************************\n'
printf 'SHADOW DOSYASI - GOREBILIYORSAK - cat /etc/shadow'
printf '\n*******************************************************\n'
cat /etc/shadow 2>/dev/null
printf '\n*******************************************************\n'
printf '/ROOT/ DIZINI ALTINDAKI DOSYALAR VE ERISIM HAKLARI - ls -ahlR /root/'
printf '\n*******************************************************\n'
ls -ahlR /root/ 2>/dev/null
printf '\n*******************************************************\n'
printf '/HOME/ DIZINI ALTINDAKI DOSYALAR VE ERISIM HAKLARI - ls -ahlR /home/'
printf '\n*******************************************************\n'
ls -ahlR /home/ 2>/dev/null
printf '\n*******************************************************\n'
printf 'EGER HOME DIZINLERI /USR/ DIZINI ALTINDA ISE BURADAKI DOSYALAR VE
ERISIM HAKLARI - ls -ahlR /usr/home/'
printf '\n*******************************************************\n'
ls -ahlR /usr/home/ 2>/dev/null
printf '\n*******************************************************\n'
printf '/HOME/ DIZINI ALTINDAKI OKUNABILIR DOSYALARIN LISTESI - find /home/ -
perm -4 -type f -exec ls -al {} \;'
printf '\nNOT: Bu komut manuel inceleme sirasında da hedef dizin adi
degistirilerek kullanilabilir'
printf '\n*******************************************************\n'
find /home/ -perm -4 -type f -exec ls -al {} \; 2>/dev/null
printf '\n*******************************************************\n'
printf 'BAZI HASSAS DOSYALARIN ERISIM HAKLARI - EKLEME YAPILABILIR'
printf '\nNOT: History dosyalari v.d. dosyalar icinde okuma hakkimiz
olanlarin icine manuel olarak goz atilmalidir'
printf '\n*******************************************************\n'
ls -la /etc/passwd 2>/dev/null
ls -la /etc/group 2>/dev/null
ls -la /etc/profile 2>/dev/null
ls -la /etc/shadow 2>/dev/null
ls -la /etc/master.passwd 2>/dev/null
ls -la /etc/sudoers 2>/dev/null
ls -la /etc/crontab 2>/dev/null
ls -la ~/.*_history 2>/dev/null
ls -la /home/*/.*_history 2>/dev/null
ls -la /root/.*_history 2>/dev/null
printf '\n*******************************************************\n'
printf 'KULLANICIMIZIN HISTORY DOSYALARI ICERIKLERI'
printf '\n*******************************************************\n'
cat ~/.*_history 2>/dev/null
printf '\n*******************************************************\n'
printf 'KULLANICIMIZIN HISTORY BILGISI - history KOMUTU CIKTISI'
printf '\n*******************************************************\n'
history 2>/dev/null
printf '\n*******************************************************\n'
printf 'OKUYABILIYORSAK ROOT UN HISTORY DOSYALARI ICERIKLERI'
printf '\n*******************************************************\n'
cat /root/.*_history 2>/dev/null
printf '\n*******************************************************\n'
printf 'OKUYABILDIGIMIZ KULLANICI HISTORY DOSYALARI ICERIKLERI'
printf '\n*******************************************************\n'
cat /home/*/.*_history 2>/dev/null
printf '\n*******************************************************\n'
printf 'TCP SERVISLERIN VE ILGILI PROSESLERIN LISTESI - netstat -antp'
printf '\n*******************************************************\n'
netstat -antp
printf '\n*******************************************************\n'
printf 'UDP SERVISLERIN VE ILGILI PROSESLERIN LISTESI - netstat –anup'
printf '\n*******************************************************\n'
netstat -anup
printf '\n*******************************************************\n'
printf 'ROOT KULLANICISI OLARAK CALISAN PROSESLER'
printf '\n*******************************************************\n'
ps aux | grep root
printf '\n*******************************************************\n'
printf 'TUM PROSESLERIN LISTESI - ps aux - ozellikle MySQL ve Apache prosesleri uzerinden islem yapmak istersek bu proseslerin hangi kullanici haklari ile calistigina dikkat edelim. Bunun disinda calisan prosesler bize baska fikirler verebilir.'
printf '\n*******************************************************\n'
ps aux
printf '\n*******************************************************\n'
printf 'CALISAN PROSESLERIN IMAJLARI VE BUNLARA ERISIM HAKLARI - ps aux | awk
{print $11}|xargs -r ls -la 2>/dev/null |awk !x[$0]++'
printf '\n*******************************************************\n'
ps aux | awk '{print $11}'|xargs -r ls -la 2>/dev/null |awk '!x[$0]++'
printf '\n*******************************************************\n'
printf 'ENVIRONMENT VARIABLE DEGERLERI'
printf '\n*******************************************************\n'
printenv
printf '\n======================================================='
printf '\nPRATIK YETKI YUKSELTME ALANLARI'
printf '\n======================================================='
printf '\n*******************************************************\n'
printf 'SAHIBI ROOT OLAN OTHER TARAFINDAN YAZILABILIR SETUID DOSYALAR - find
/ -uid 0 -perm -4002 -type f -exec ls -al {} \;'
printf '\n*******************************************************\n'
find / -uid 0 -perm -4002 -type f -exec ls -al {} \; 2>/dev/null
printf '\n*******************************************************\n'
printf 'OTHER TARAFINDAN YAZILABILIR TUM SETUID DOSYALAR - find / -perm -4002-type f -exec ls -al {} \;'
printf '\n*******************************************************\n'
find / -perm -4002 -type f -exec ls -al {} \; 2>/dev/null
printf '\n*******************************************************\n'
printf 'TUM SETUID DOSYALAR - find / -perm -4000 -type f -exec ls -al {} \;
Bu dosyalar arasinda grubumuzun yazma hakki olanlara da dikkat edelim, cunku
bu durum icin ozel bir sorgumuz yok'
printf '\n*******************************************************\n'
find / -perm -4000 -type f -exec ls -al {} \; 2>/dev/null | tee setuid-filesenum.txt
printf '\n*******************************************************\n'
printf 'SHELL ESCAPE IMKANI VEREN SETUID DOSYALAR - False positive satirlari
elle incelemek gereklidir, aradigimiz uygulama isimleri icin scripti
okuyunuz'
printf '\n*******************************************************\n'
cat setuid-files-enum.txt 2>/dev/null | grep -i -E 'vi|awk|perl|find|nmap|man|more|less|tcpdump|bash|sh$|vim|nc$|netcat|python|ruby|lua|irb' | grep -v -E 'chsh|device'
printf '\n*******************************************************\n'
printf 'SAHIBI ROOT OLAN OTHER TARAFINDAN YAZILABILIR SETGID DOSYALAR - find/ -uid 0 -perm -2002 -type f -exec ls -al {} \;'
printf '\n*******************************************************\n'
find / -uid 0 -perm -2002 -type f -exec ls -al {} \; 2>/dev/null
printf '\n*******************************************************\n'
printf 'OTHER TARAFINDAN YAZILABILIR TUM SETGID DOSYALAR - find / -perm -2002 -type f'
printf '\n*******************************************************\n'
find / -perm -2002 -type f -exec ls -al {} \; 2>/dev/null
printf '\n*******************************************************\n'
printf 'SETGID ISARETLI TUM DOSYALAR - find / -perm -2000 -type f -exec ls -al {} \;'
printf '\n*******************************************************\n'
find / -perm -2000 -type f -exec ls -al {} \; 2>/dev/null
printf '\n*******************************************************\n'
printf '/ETC/CRON DIZINLERINDE BULUNAN DOSYALAR VE ERISIM HAKLARI - ls -la /etc/cron*'
printf '\n*******************************************************\n'
ls -la /etc/cron* 2>/dev/null
printf '\n*******************************************************\n'
printf 'OTHER TARAFINDAN YAZILABILIR CRON SCRIPTLERI VE ICERIKLERI - find
/etc/cron* -perm -0002 -exec ls -la {} \; -exec cat {} 2>/dev/null \;'
printf '\n*******************************************************\n'
find /etc/cron* -perm -0002 -exec ls -la {} \; -exec cat {} 2>/dev/null \;
printf '\n*******************************************************\n'
printf '/ETC/CRONTAB DOSYASI ICERIGI - cat /etc/crontab'
printf '\n*******************************************************\n'
cat /etc/crontab 2>/dev/null
printf '\n*******************************************************\n'
printf 'VARSA ROOT VE DIGER KULLANICILARIN CRONTAB DOSYALARI LISTESI - ls -laR /var/spool/cron'
printf '\n*******************************************************\n'
ls -laR /var/spool/cron 2>/dev/null
printf '\n*******************************************************\n'
printf 'VARSA ROOT VE DIGER KULLANICILARIN CRONTAB DOSYALARI ICERIKLERI'
printf '\n*******************************************************\n'
find /var/spool/cron/ -type f -exec tail -n +1 {} + 2>/dev/null
printf '\n*******************************************************\n'
printf 'VARSA /etc/cron.d DIZININDE BULUNAN DOSYALARIN LISTESI - ls -laR
/etc/cron.d'
printf '\n*******************************************************\n'
ls -laR /etc/cron.d 2>/dev/null
printf '\n*******************************************************\n'
printf 'VARSA /etc/cron.d DIZININDE BULUNAN DOSYALARIN ICERIKLERI'
printf '\n*******************************************************\n'
find /etc/cron.d/ -type f -exec tail -n +1 {} + 2>/dev/null
printf '\n*******************************************************\n'
printf '/ETC/ANACRONTAB DOSYASI ICERIGI - cat /etc/anacrontab'
printf '\n*******************************************************\n'
cat /etc/anacrontab 2>/dev/null
printf '\n*******************************************************\n'
printf 'VARSA KULLANICILARIN AKTIF CRON KONFIGURASYONLARI - cat /etc/passwd |
cut -d : -f 1 | xargs -n1 crontab -l -u'
printf '\n*******************************************************\n'
cat /etc/passwd | cut -d ":" -f 1 | xargs -n1 crontab -l -u 2>/dev/null
printf '\n*******************************************************\n'
printf 'MYSQL E ROOT - ROOT ERISIM BILGILERIYLE ERISEBILIYOR MUYUZ -mysqladmin -uroot -proot version'
printf '\n*******************************************************\n'
mysqladmin -uroot -proot version
printf '\n*******************************************************\n'
printf 'MYSQL E BOS PAROLA ILE ROOT OLARAK ERISEBILIYOR MUYUZ - mysqladmin -uroot version'
printf '\n*******************************************************\n'
mysqladmin -uroot version
printf '\n*******************************************************\n'
printf '*** Postgre SQL varsa onun icin de ayrica komutlar calistirilabilir,process listesine gore hareket etmek lazim ***'
printf '\n*******************************************************\n'
printf '\n*******************************************************\n'
printf 'VERSIYON BILGILERI - TOPLUCA'
printf '\n*******************************************************\n'
printf '\nSUDO - VERSIYON - PRIVESC ACIKLIKLARINI KONTROL ET http://www.exploitdb.com/search/?action=search&filter_page=1&filter_description=sudo'
printf '\n..................................\n'
sudo -V | grep version 2>/dev/null
printf '\nMYSQL - VERSIYON'
printf '\n..................................\n'
mysql --version 2>/dev/null
printf '\nPOSTGRESQL - VERSIYON'
printf '\n..................................\n'
psql -V
printf '\nAPACHE - VERSIYON'
printf '\n..................................\n'
apache2 -v 2>/dev/null; apache2ctl -M 2>/dev/null; httpd -v 2>/dev/null;
apachectl -l 2>/dev/null
printf '\nPERL - VERSIYON'
printf '\n..................................\n'
perl -v 2>/dev/null
printf '\nJAVA - VERSIYON'
printf '\n..................................\n'
java -version 2>/dev/null
printf '\nPYTHON - VERSIYON'
printf '\n..................................\n'
python --version 2>/dev/null
printf '\nRUBY - VERSIYON'
printf '\n..................................\n'
ruby -v 2>/dev/null
printf '\n======================================================='
printf '\nUZUN INCELEME'
printf '\n======================================================='
printf '\n*******************************************************\n'
printf 'DIZIN VE DOSYA LISTESINI OLUSTURUYORUZ - find / > dirlist-enum.txt'
printf '\n*******************************************************\n'
find / > dirlist-enum.txt 2>/dev/null
printf 'dirlist-enum.txt dosyasi olusturuldu.\n'
printf '\n*******************************************************\n'
printf 'SONU INI ILE BITEN DOSYALARIN LISTESI - grep -i -E ini$ dirlistenum.txt > ini-files-enum.txt'
printf '\nNOT: Uzun suren incelemelerde ini, conf, backup v.b. dosyalarin icerigini manuel olarak inceleyiniz.'
printf '\n*******************************************************\n'
grep -i -E 'ini$' dirlist-enum.txt > ini-files-enum.txt
printf 'ini-files-enum.txt dosyasi olusturuldu.\n'
printf '\n*******************************************************\n'
printf 'SONU CONF, CONFIG VE CNF ILE BITEN DOSYALARIN LISTESI - grep -i -E conf$|config$|cnf$ dirlist-enum.txt > conf-files-enum.txt'
printf '\n*******************************************************\n'
grep -i -E 'conf$|config$|cnf$' dirlist-enum.txt > conf-files-enum.txt
printf 'conf-files-enum.txt dosyasi olusturuldu.\n'
printf '\n*******************************************************\n'
printf 'SONU BACKUP, BCK, BAK, OLD ILE BITEN DOSYALARIN LISTESI - grep -i -E backup$|bck$|bak$|old$ dirlist-enum.txt > backup-files-enum.txt'
printf '\n*******************************************************\n'
grep -i -E 'backup$|bck$|bak$|\.old.*$' dirlist-enum.txt > backup-filesenum.txt
printf 'backup-files-enum.txt dosyasi olusturuldu.\n'
printf '\n*******************************************************\n'
printf 'SONU CAP ILE BITEN DOSYALARIN LISTESI - grep -i -E cap$ dirlistenum.txt > capture-files-enum.txt - dosya tipinden emin olmak icin file komutunu kullanabilirsiniz'
printf '\n*******************************************************\n'
grep -i -E 'cap$' dirlist-enum.txt > capture-files-enum.txt
printf 'capture-files-enum.txt dosyasi olusturuldu.\n'
printf '\n*******************************************************\n'
printf 'SONU .PHP ILE BITEN DOSYALARIN LISTESI - grep -i -E .php$ dirlistenum.txt > php-files-enum.txt'
printf '\n*******************************************************\n'
grep -i -E '\.php$' dirlist-enum.txt > php-files-enum.txt
printf 'php-files-enum.txt dosyasi olusturuldu.\n'
printf '\n*******************************************************\n'
printf 'SONU .PL ILE BITEN DOSYALARIN LISTESI - grep -i -E .pl$ dirlistenum.txt > pl-files-enum.txt'
printf '\n*******************************************************\n'
grep -i -E '\.pl$' dirlist-enum.txt > pl-files-enum.txt
printf 'pl-files-enum.txt dosyasi olusturuldu.\n'
printf '\n*******************************************************\n'
printf 'SONU .SH ILE BITEN DOSYALARIN LISTESI - grep -i -E .sh$ dirlistenum.txt > sh-files-enum.txt'
printf '\n*******************************************************\n'
grep -i -E '\.sh$' dirlist-enum.txt > sh-files-enum.txt
printf 'sh-files-enum.txt dosyasi olusturuldu.\n'
printf '\n*******************************************************\n'
printf 'SONU LOG ILE BITEN DOSYALARIN LISTESI - grep -i -E log$ dirlistenum.txt > log-files-enum.txt'
printf '\n*******************************************************\n'
grep -i -E 'log$' dirlist-enum.txt > log-files-enum.txt
printf 'log-files-enum.txt dosyasi olusturuldu.\n'
printf '\n*******************************************************\n'
printf 'SONU INC ILE BITEN DOSYALARIN LISTESI - grep -i -E log$ dirlistenum.txt > inc-files-enum.txt'
printf '\n*******************************************************\n'
grep -i -E 'inc$' dirlist-enum.txt > inc-files-enum.txt
printf 'inc-files-enum.txt dosyasi olusturuldu.\n'
printf 'SONU MYD ILE BITEN DOSYALARIN LISTESI - grep -i -E myd$ dirlistenum.txt > myd-files-enum.txt'
printf '\n*******************************************************\n'
grep -i -E 'myd$' dirlist-enum.txt > myd-files-enum.txt
printf 'myd-files-enum.txt dosyasi olusturuldu.\n'
printf '\n*******************************************************\n'
printf 'ICINDE SHADOW GECEN DIZIN VEYA DOSYALARIN LISTESI - grep -i -E ini$ dirlist-enum.txt > ini-files-enum.txt'
printf '\n*******************************************************\n'
grep -i -E 'shadow' dirlist-enum.txt | xargs ls -al 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICINDE PASS GECEN DIZIN VEYA DOSYALARIN LISTESI'
printf '\n*******************************************************\n'
grep -i -E 'pass' dirlist-enum.txt | xargs ls -al 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICINDE CRON GECEN DIZIN VEYA DOSYALARIN LISTESI - Bu dosyalara manuel olarak bakilmalidir'
printf '\n*******************************************************\n'
grep -i -E 'cron' dirlist-enum.txt | xargs ls -al 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICINDE HISTORY GECEN DIZIN VEYA DOSYALARIN LISTESI'
printf '\n*******************************************************\n'
grep -i -E 'history' dirlist-enum.txt | xargs ls -al 2>/dev/null
printf '\n*******************************************************\n'
printf 'MY.CNF ADLI DOSYALARIN LISTESI'
printf '\n*******************************************************\n'
grep -i -E 'my\.cnf$' dirlist-enum.txt | xargs -r ls -al 2>/dev/null
printf '\n*******************************************************\n'
printf 'MY.CONF ADLI DOSYALARIN LISTESI'
printf '\n*******************************************************\n'
grep -i -E 'my\.conf$' dirlist-enum.txt | xargs -r ls -al 2>/dev/null
printf '\n*******************************************************\n'
printf '==OZET PASSWORD SATIRLARI=='
printf '\n*******************************************************\n'
printf '\n*******************************************************\n'
printf 'INI DOSYALARI ICINDE GECEN PASSWORD VE USERNAME SATIRLARI'
printf '\n*******************************************************\n'
cat ini-files-enum.txt | xargs grep -i -E 'pass =|passwd =|pwd =| password =|user =|username =|pass=|passwd=|pwd=|password=|user=|username=|mysql_connect|mysql_select_db' 2>/dev/null
printf '\n*******************************************************\n'
printf 'CONF DOSYALARI ICINDE GECEN PASSWORD VE USERNAME SATIRLARI'
printf '\n*******************************************************\n'
cat conf-files-enum.txt | xargs grep -i -E 'pass =|passwd =|pwd =| password =|user =|username =|pass=|passwd=|pwd=|password=|user=|username=|mysql_connect|mysql_select_db' 2>/dev/null
printf '\n*******************************************************\n'
printf 'PHP DOSYALARI ICINDE GECEN PASSWORD VE USERNAME SATIRLARI'
printf '\n*******************************************************\n'
cat php-files-enum.txt | xargs grep -i -E 'pass =|passwd =|pwd =| password =|user =|username =|pass=|passwd=|pwd=|password=|user=|username=|mysql_connect|mysql_select_db' 2>/dev/null
printf '\n*******************************************************\n'
printf 'PERL DOSYALARI ICINDE GECEN PASSWORD VE USERNAME SATIRLARI'
printf '\n*******************************************************\n'
cat pl-files-enum.txt | xargs grep -i -E 'pass =|passwd =|pwd =| password =|user =|username =|pass=|passwd=|pwd=|password=|user=|username=|mysql_connect|mysql_select_db' 2>/dev/null
printf '\n*******************************************************\n'
printf 'SH DOSYALARI ICINDE GECEN PASSWORD VE USERNAME SATIRLARI'
printf '\n*******************************************************\n'
cat sh-files-enum.txt | xargs grep -i -E 'pass =|passwd =|pwd =| password =|user =|username =|pass=|passwd=|pwd=|password=|user=|username=|mysql_connect|mysql_select_db' 2>/dev/null
printf '\n*******************************************************\n'
printf 'LOG DOSYALARI ICINDE GECEN PASSWORD VE USERNAME SATIRLARI'
printf '\n*******************************************************\n'
cat log-files-enum.txt | xargs grep -i -E 'pass =|passwd =|pwd =| password =|user =|username =|pass=|passwd=|pwd=|password=|user=|username=|mysql_connect|mysql_select_db' 2>/dev/null
printf '\n*******************************************************\n'
printf 'INC DOSYALARI ICINDE GECEN PASSWORD VE USERNAME SATIRLARI'
printf '\n*******************************************************\n'
cat inc-files-enum.txt | xargs grep -i -E 'pass =|passwd =|pwd =| password =|user =|username =|pass=|passwd=|pwd=|password=|user=|username=|mysql_connect|mysql_select_db' 2>/dev/null
printf '\n*******************************************************\n'
printf 'MYD DOSYALARI ICINDE GECEN PASSWORD VE USERNAME SATIRLARI'
printf '\n*******************************************************\n'
cat myd-files-enum.txt | xargs grep -i -E 'pass =|passwd =|pwd =| password =|user =|username =|pass=|passwd=|pwd=|password=|user=|username=|mysql_connect|mysql_select_db' 2>/dev/null
printf '\n*******************************************************\n'
printf '/ETC DIZINI ALTINDA SONU .CONF* ILE BITEN DOSYALARIN LISTESI VE
ERISIM HAKLARI - find /etc/ -maxdepth 4 -name *.conf* -type f -exec ls -la {}
\;'
printf '\nNOT: Belli bir isim yapisindaki dosyalarin erisim haklarini
listelemek icin dirlist-enum.txt dosyasinden filtrelenmis dosya adlarini
kullanabiliriz.'
printf '\nOrnegin: cat ini-files-enum.txt | xargs ls -al komutuyla sonu ini
ile biten dosyalarin erisim haklarinin listelenmesi gibi'
printf '\n*******************************************************\n'
find /etc/ -maxdepth 4 -name *.conf* -type f -exec ls -la {} \; 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICERIK - /var/mail/root'
printf '\n*******************************************************\n'
cat /var/mail/root 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICERIK - /var/spool/mail/root'
printf '\n*******************************************************\n'
cat /var/spool/mail/root 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICERIK - /etc/syslog.conf'
printf '\n*******************************************************\n'
cat /etc/syslog.conf 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICERIK - /etc/chttp.conf'
printf '\n*******************************************************\n'
cat /etc/chttp.conf 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICERIK - /etc/lighttpd.conf'
printf '\n*******************************************************\n'
cat /etc/lighttpd.conf 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICERIK - /etc/cups/cupsd.conf'
printf '\n*******************************************************\n'
cat /etc/cups/cupsd.conf 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICERIK - /etc/inetd.conf'
printf '\n*******************************************************\n'
cat /etc/inetd.conf 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICERIK - /etc/apache2/apache2.conf'
printf '\n*******************************************************\n'
cat /etc/apache2/apache2.conf 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICERIK - /etc/mysql/my.cnf ve /etc/my.cnf'
printf '\n*******************************************************\n'
cat /etc/mysql/my.cnf 2>/dev/null
cat /etc/my.cnf 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICERIK - /etc/my.conf'
printf '\n*******************************************************\n'
cat /etc/my.conf 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICERIK - /etc/httpd/conf/httpd.conf'
printf '\n*******************************************************\n'
cat /etc/httpd/conf/httpd.conf 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICERIK - /opt/lampp/etc/httpd.conf'
printf '\n*******************************************************\n'
cat /opt/lampp/etc/httpd.conf 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICERIK - /var/apache2/config.inc'
printf '\n*******************************************************\n'
cat /var/apache2/config.inc 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICERIK - /var/lib/mysql/mysql/user.MYD'
printf '\n*******************************************************\n'
cat /var/lib/mysql/mysql/user.MYD 2>/dev/null
printf '\n*******************************************************\n'
printf 'ICERIK - /root/anaconda-ks.cfg'
printf '\n*******************************************************\n'
cat /root/anaconda-ks.cfg 2>/dev/null
printf '\n*******************************************************\n'
printf 'KULLANICIMIZA AIT OLMAYAN ANCAK YAZMA HAKKIMIZ OLAN TUM DOSYALARIN
LISTESI VE ERISIM HAKLARI - find / -writable -not -user whoami -type f -not -
path /proc/* -exec ls -al {} \;'
printf '\n*******************************************************\n'
find / -writable -not -user `whoami` -type f -not -path "/proc/*" -exec ls -al {} \; 2>/dev/null
printf '\n*******************************************************\n'
printf 'TUM WORLD WRITABLE DOSYALARIN LISTESI VE ERISIM HAKLARI - find / ! -
path */proc/* -perm -2 -type f -exec ls -al {} \;'
printf '\n*******************************************************\n'
find / ! -path "*/proc/*" -perm -2 -type f -exec ls -al {} \; 2>/dev/null
printf '\n*******************************************************\n'
printf 'HERKESIN YAZABILECEGI DIZINLERIN LISTESI'
printf '\n*******************************************************\n'
find / -type d -not -path "/proc/*" \( -perm -o+w \) -exec ls -ald {} \; 2>/dev/null
printf '\n*******************************************************\n'
printf 'BIZIM YAZABILECEGIMIZ DIZINLERIN LISTESI - find / -writable -type d -
not -path /proc/* -exec ls -al {} \;'
printf '\nManuel olarak script lerimizi ve ciktilarini yerlestirebilecegimiz
bir dizin bulmak icin de kullanilabilir'
printf '\n*******************************************************\n'
find / -writable -type d -not -path "/proc/*" -exec ls -ald {} \; 2>/dev/null
printf '\n*******************************************************\n'
printf 'KULLANICIMIZA AIT DIZINLERIN LISTESI - find / -user whoami -type d - not -path /proc/* -exec ls -al {} \;'
printf '\n*******************************************************\n'
find / -user `whoami` -type d -not -path "/proc/*" -exec ls -ald {} \; 2>/dev/null
printf '\n*******************************************************\n'
printf 'SSH ANAHTAR VE ANAHTAR DIZINLERININ LISTESI - find / -name id_dsa* -o
-name id_rsa* -o -name known_hosts -o -name authorized_hosts -o -name
authorized_keys: Ozel ve acik anahtar kavramlari ile bunlarin SSH da nasil
kullanıldigi ile ilgili on bilgi edinmenizde fayda var'
printf '\n*******************************************************\n'
find / -name "id_dsa*" -o -name "id_rsa*" -o -name "known_hosts" -o -name "authorized_hosts" -o -name "authorized_keys" 2>/dev/null
printf '\n*******************************************************\n'
printf 'SSH SERVISINE ROOT KULLANICISI OLARAK BAGLANABILIR MIYIZ - grep
PermitRootLogin /etc/ssh/sshd_config 2>/dev/null | grep -v | awk {print
$2}: Gecerli degerler yes, without-password, forced-commands-only, veya no
dur. without-password private key ile erisilebilir anlamina gelir. forcedcommands-only
yapilabilecek islemleri kisitlar ve private key ile
gelinmelidir.'
printf '\n*******************************************************\n'
grep "PermitRootLogin " /etc/ssh/sshd_config 2>/dev/null | grep -v '\#' | awk '{print $2}'
printf '\n*******************************************************\n'
printf 'SSH KONFIGURASYON DIZINI ERISIM HAKLARIMIZ - ls -la /etc/ssh/'
printf '\nBu baglamda root un home dizinindeki authorized keys dizinine
yazabiliyorsak asagidaki linklerden faydalanarak sirasiyla key uretebilir ve
yerlestirebiliriz'
printf '\nhttp://www.thegeekstuff.com/2008/11/3-steps-to-perform-ssh-loginwithout-password-using-ssh-keygen-ssh-copy-id/'
printf '\nhttp://www.rebol.com/docs/ssh-auto-login.html'
printf '\n*******************************************************\n'
ls -la /etc/ssh/ 2>/dev/null
printf '\n*******************************************************\n'
printf 'SHELL UYGULAMALARININ LISTESI - cat /etc/shells'
printf '\n*******************************************************\n'
cat /etc/shells | xargs ls -al 2>/dev/null
printf '\n*******************************************************\n'
printf 'KULLANICIMIZIN PATH CEVRESEL DEGISKENI - echo $PATH'
printf '\n*******************************************************\n'
echo $PATH
printf '\n*******************************************************\n'
printf 'PAROLA POLITIKASI, PAROLA HASH ALGORITMASI V.D. BILGILER - cat
/etc/login.defs'
printf '\n*******************************************************\n'
cat /etc/login.defs
printf '\n*******************************************************\n'
printf 'APACHE PROCESS ININ HANGI KULLANICI OLARAK KONFIGURE EDILDIGI - cat
/etc/apache2/envvars 2>/dev/null |grep -i user\|group |awk {sub(/.*\export
/,)}1 Gercek kullanici bilgisine ps aux ciktisindan erisebiliriz'
printf '\n*******************************************************\n'
cat /etc/apache2/envvars 2>/dev/null |grep -i 'user\|group' |awk '{sub(/.*\export /,"")}1'
printf '\n*******************************************************\n'
printf 'GOREBILDIGIMIZ TUM HOME DIZINLERI ALTINDA VARSA RHOSTS DOSYALARI -
find /home -iname *.rhosts -exec ls -la {} 2>/dev/null \; -exec cat {} 2>/dev/null \;'
printf '\n*******************************************************\n'
find /home -iname *.rhosts -exec ls -la {} 2>/dev/null \; -exec cat {} 2>/dev/null \;
printf '\n*******************************************************\n'
printf 'EGER HOME DIZINLERI /USR/ DIZINI ALTINDA ISE GOREBILDIGIMIZ HOME
DIZINLERI ALTINDA VARSA RHOSTS DOSYALARI - find /usr/home -iname *.rhosts -
exec ls -la {} 2>/dev/null \; -exec cat {} 2>/dev/null \;'
printf '\n*******************************************************\n'
find /usr/home -iname *.rhosts -exec ls -la {} 2>/dev/null \; -exec cat {} 2>/dev/null \;
printf '\n*******************************************************\n'
printf 'HOSTS.EQUIV DOSYASININ ERISIM HAKKI VE GOREBILIYORSAK ICERIGI - find
/etc -iname hosts.equiv -exec ls -la {} 2>/dev/null \; -exec cat {}
2>/dev/null \;'
printf '\n*******************************************************\n'
find /etc -iname hosts.equiv -exec ls -la {} 2>/dev/null \; -exec cat {} 2>/dev/null \;
printf '\n*******************************************************\n'
printf 'EXPORTS DOSYASININ ERISIM HAKLARI - ls -la /etc/exports'
printf '\n*******************************************************\n'
ls -la /etc/exports 2>/dev/null
printf '\n*******************************************************\n'
printf 'OKUYABILIYORSAK EXPORTS DOSYASININ ICERIGI - cat /etc/exports'
printf '\n*******************************************************\n'
cat /etc/exports 2>/dev/null
printf '\n*******************************************************\n'
printf 'VARSA /VAR/MAIL DIZINI ALTINDAKI DOSYALAR VE ERISIM HAKLARI - ls -la
/var/mail - Bu dosyalara manuel olarak bakmak gerekebilir'
printf '\n*******************************************************\n'
ls -la /var/mail 2>/dev/null
printf '\n*******************************************************\n'
printf 'VARSA /VAR/SPOOL/MAIL DIZINI ALTINDAKI DOSYALAR VE ERISIM HAKLARI -
ls -la /var/spool/mail - Bu dosyalara manuel olarak bakmak gerekebilir'
printf '\n*******************************************************\n'
ls -la /var/spool/mail 2>/dev/null
printf '\n*******************************************************\n'
printf 'VARSA VE OKUYABILIYORSAK ROOT UN MAIL KUTUSUNUN ILK BOLUMU - head
/var/mail/root'
printf '\n*******************************************************\n'
head /var/mail/root 2>/dev/null
printf '\n*******************************************************\n'
printf 'VARSA VE OKUYABILIYORSAK ROOT UN MAIL KUTUSUNUN ILK BOLUMU - head
/var/spool/mail/root'
printf '\n*******************************************************\n'
head /var/spool/mail/root 2>/dev/null
printf '\n*******************************************************\n'
printf 'INETD DOSYASININ ICERIGI - cat /etc/inetd.conf - otomatik baslatilan
ag servisleri icin'
printf '\n*******************************************************\n'
cat /etc/inetd.conf 2>/dev/null
printf '\n*******************************************************\n'
printf 'TCP WRAPPER UYGULAYAN SISTEMLER ICIN XINETD DOSYASININ ICERIGI - cat
/etc/xinetd.conf'
printf '\n*******************************************************\n'
cat /etc/xinetd.conf 2>/dev/null
printf '\n*******************************************************\n'
printf 'INIT.D DIZINI ALTINDAKI SCRIPTLER VE ERISIM IZINLERI - ls -la
/etc/init.d - linux uzerine kurulmus servisler hakkinda fikir verir, buradaki
scriptlerin hepsi calismiyor olabilir. Bu dosyalar icinde grep ile kelime
aranabilir'
printf '\n*******************************************************\n'
ls -la /etc/init.d 2>/dev/null
printf '\n*******************************************************\n'
printf 'DUSUK BIR IHTIMAL AMA INIT SCRIPTLERI ICINDE BIR PAROLA OLABILIR MI'
printf '\n*******************************************************\n'
ls /etc/init.d 2>/dev/null| xargs grep -i -E 'pass =|passwd =|pwd =| password =|pass=|passwd=|pwd=|password=' 2>/dev/null
printf '\n*******************************************************\n'
printf 'ROOT KULLANICISINA AIT OLMAYAN ANCAK INIT.D DIZINI ALTINDA BULUNAN
DOSYALARIN LISTESI - find /etc/init.d/ \! -uid 0 -type f 2>/dev/null |xargs -
r ls -la 2>/dev/null'
printf '\n*******************************************************\n'
find /etc/init.d/ \! -uid 0 -type f 2>/dev/null |xargs -r ls -la 2>/dev/null
printf '\n*******************************************************\n'
printf 'INIT SCRIPTLERI RC.D DIZINLERI ALTINDA BULUNAN SISTEMLER ICIN INIT
SCRIPTLERI LISTESI VE ERISIM HAKLARI - ls -la /etc/rc.d/init.d'
printf '\n*******************************************************\n'
ls -la /etc/rc.d/init.d 2>/dev/null
printf '\n*******************************************************\n'
printf 'ROOT KULLANICISINA AIT OLMAYAN ANCAK RC.D/INIT.D DIZINI ALTINDA
BULUNAN DOSYALARIN LISTESI - find /etc/rc.d/init.d \! -uid 0 -type f
2>/dev/null |xargs -r ls -la 2>/dev/null'
printf '\n*******************************************************\n'
find /etc/rc.d/init.d \! -uid 0 -type f 2>/dev/null |xargs -r ls -la 2>/dev/null
printf '\n*******************************************************\n'
printf 'MOUNT KONFIGURASYONU - cat /etc/fstab *** ONEMLI - REISERFS GIBI
SIRADISI FILE SYSTEM GORURSENIZ EXPLOIT ETMEYI DENEYIN'
printf '\n*******************************************************\n'
cat /etc/fstab 2>/dev/null
printf '\n======================================================='
printf '\nEK BILGI'
printf '\n======================================================='
printf '\n*******************************************************\n'
printf 'TUM AG ARAYUZLERININ LISTESI - /sbin/ifconfig -a'
printf '\n*******************************************************\n'
/sbin/ifconfig -a
printf '\n*******************************************************\n'
printf 'SUNUCUDA TANIMLI ROUTE BILGILERI - route'
printf '\n*******************************************************\n'
/sbin/route 2>/dev/null
printf '\n*******************************************************\n'
printf 'MOUNT EDILMIS PARTITION LAR - mount'
printf '\n*******************************************************\n'
mount 2>/dev/null
printf '\n*******************************************************\n'
printf 'MOUNT EDILMIS PARTITION LAR VE KULLANIM ORANLARI - df -h'
printf '\n*******************************************************\n'
df -h 2>/dev/null
printf '\n*******************************************************\n'
printf 'DOSYA TRANSFER ARACLARIMIZ NELER'
printf '\nNOT: Path cevresel degiskenimiz yeterli degilse which komutlari var
oldugu halde dosya transfer araclarini bulamayabilir, bu bolumdeki ciktilari
bu acidan degerlendirmelisiniz.'
printf '\n*******************************************************\n'
which nc
which netcat
which wget
which tftp
which ftp
printf '\n*******************************************************\n'
printf 'KURULU PAKETLER VE VERSIYONLARI'
printf '\n*******************************************************\n'
if grep -q -E -i 'ubuntu|debian' /proc/version;
then
 dpkg -l 2>/dev/null
else
 rpm -qa 2>/dev/null
fi
printf '\n*******************************************************\n'
printf 'WEB UYGULAMA DIZINLERI VE DOSYALARIN LISTESI - EKLEME YAPILABILIR'
printf 'NOT: Bu dizinlere manuel olarak goz atilmalidir'
printf '\n*******************************************************\n'
ls -alhR /var/www/ 2>/dev/null
ls -alhR /srv/www/htdocs/ 2>/dev/null
ls -alhR /usr/local/www/apache22/data/ 2>/dev/null
ls -alhR /opt/lampp/htdocs/ 2>/dev/null
printf '\n*******************************************************\n'
printf '==DETAYLI PASSWORD VE ROOT KELIMELERI GECEN SATIRLAR=='
printf '\n*******************************************************\n'
printf '\n*******************************************************\n'
printf 'INI DOSYALARI ICINDE PASS, PWD, ROOT VE ADMIN KELIMELERI GECEN
SATIRLAR - cat ini-files-enum.txt | xargs grep -E pass|pwd|root'
printf '\nNOT: grep ile aranan kelimelerin gectigi satirlar yerine sadece bu
kelimelerin gectigi dosyalari gormek istiyorsaniz grep -l komutunu
kullanabilirsiniz'
printf '\nNOT: Manuel olarak belli kelimeleri belli dosyalar icinde aramak
icin su komut kullanilabilir, arama terimlerini tek tirnak icine almayi
unutmayiniz: find / -name *.conf* -type f -exec grep -Hn password|root {} \;
2>/dev/null '
printf '\n*******************************************************\n'
cat ini-files-enum.txt | xargs grep -i -E 'pass|pwd|root|admin' 2>/dev/null | grep '='
printf '\n*******************************************************\n'
printf 'CONF DOSYALARI ICINDE PASS, PWD, ROOT VE ADMIN KELIMELERI GECEN
SATIRLAR - cat conf-files-enum.txt | xargs grep -E pass|pwd|root'
printf '\n*******************************************************\n'
cat conf-files-enum.txt | xargs grep -i -E 'pass|pwd|root|admin' 2>/dev/null | grep '='
printf '\n*******************************************************\n'
printf 'PHP DOSYALARI ICINDE PASS, PWD, ROOT VE ADMIN KELIMELERI GECEN
SATIRLAR - cat php-files-enum.txt | xargs grep -E pass|pwd|rootr'
printf '\n*******************************************************\n'
cat php-files-enum.txt | xargs grep -i -E 'pass|pwd|root|admin' 2>/dev/null | grep '='
printf '\n*******************************************************\n'
printf 'PL DOSYALARI ICINDE PASS, PWD, ROOT VE ADMIN KELIMELERI GECEN
SATIRLAR - cat pl-files-enum.txt | xargs grep -E pass|pwd|root'
printf '\n*******************************************************\n'
cat pl-files-enum.txt | xargs grep -i -E 'pass|pwd|root|admin' 2>/dev/null | grep '='
printf '\n*******************************************************\n'
printf 'SH DOSYALARI ICINDE PASS, PWD, ROOT VE ADMIN KELIMELERI GECEN
SATIRLAR - cat sh-files-enum.txt | xargs grep -E pass|pwd|root'
printf '\n*******************************************************\n'
cat sh-files-enum.txt | xargs grep -i -E 'pass|pwd|root|admin' 2>/dev/null | grep '='
printf '\n*******************************************************\n'
printf 'LOG DOSYALARI ICINDE PASS, PWD, ROOT VE ADMIN KELIMELERI GECEN
SATIRLAR - cat log-files-enum.txt | xargs grep -E pass|pwd|root'
printf '\n*******************************************************\n'
cat log-files-enum.txt | xargs grep -i -E 'pass|pwd|root|admin' 2>/dev/null | grep '='
printf '\n*******************************************************\n'
printf 'INC DOSYALARI ICINDE PASS, PWD, ROOT VE ADMIN KELIMELERI GECEN
SATIRLAR - cat inc-files-enum.txt | xargs grep -E pass|pwd|root'
printf '\n*******************************************************\n'
cat inc-files-enum.txt | xargs grep -i -E 'pass|pwd|root|admin' 2>/dev/null | grep '='
printf '\n*******************************************************\n'
printf 'MYD DOSYALARI ICINDE PASS, PWD, ROOT VE ADMIN KELIMELERI GECEN
SATIRLAR - cat myd-files-enum.txt | xargs grep -E pass|pwd|root'
printf '\n*******************************************************\n'
cat myd-files-enum.txt | xargs grep -i -E 'pass|pwd|root|admin' 2>/dev/null | grep '='
printf '\n*******************************************************\n'
printf '/root/ DIZINI ALTINDA OKUYABILDIGIMIZ DOSYALARIN ICERIKLERI'
printf '\n*******************************************************\n'
find /root/ -type f -exec tail -n +1 {} + > rootfiles-enum.txt 2>/dev/null
printf '\n*******************************************************\n'
printf '/home/ DIZINI ALTINDA OKUYABILDIGIMIZ DOSYALARIN ICERIKLERI -
***ONEMLI*** EGER SCRIPTI HOME DIZINI ALTINDA CALISTIRIRSANIZ KENDINIZE DOS
YAPMIS OLURSUNUZ CUNKU SCRIPT KENDI YAZDIKLARINI TEKRAR OKUYUP TEKRAR YAZAR
VE DISKI DOLDURURSUNUZ'
printf '\n*******************************************************\n'
find /home/ -type f -exec tail -n +1 {} + > homefiles-enum.txt 2>/dev/null
printf '\n*******************************************************\n'
printf '/etc/cron* DIZINLERI ALTINDA OKUYABILDIGIMIZ DOSYALARIN ICERIKLERI'
printf '\n*******************************************************\n'
find /etc/cron* -type f -exec tail -n +1 {} + > etccronfiles-enum.txt 2>/dev/null
printf '\n======================================================='
printf '\nSCRIPT TAMAMLANDI'
printf '\n======================================================='
printf '\nBULDUGUNUZ PAROLALARI ROOT KULLANICISINA VE SISTEM UZERINDE TANIMLI
DIGER KULLANICILARA SU YAPARAK DENEMEYI UNUTMAYIN\n'

