# Testing for configuration management (OWASP Guide)

## Table of content

- [Test Network/Infrastructure Configuration (OTG-CONFIG-001)](#test-network-infrastructure-configuration--otg-config-001-)
  - [How to Test](#how-to-test)
- [Test Application Platform Configuration (OTG-CONFIG-002)](#test-application-platform-configuration--otg-config-002-)
  - [How to Test](#how-to-test-1)
    - [Black Box Testing](#black-box-testing)
    - [Gray Box Testing](#gray-box-testing)
- [Test File Extensions Handling for Sensitive Information (OTG-CONFIG-003)](#test-file-extensions-handling-for-sensitive-information--otg-config-003-)
  - [How to Test](#how-to-test-2)
  - [Tools](#tools)
- [Review Old, Backup and Unreferenced Files for Sensitive Information (OTG-CONFIG-004)](#review-old--backup-and-unreferenced-files-for-sensitive-information--otg-config-004-)
  - [Summary](#summary)
  - [Threats](#threats)
  - [How to Test](#how-to-test-3)
    - [Black Box Testing](#black-box-testing-1)
      - [Inference from the naming scheme used for published content](#inference-from-the-naming-scheme-used-for-published-content)
      - [Other clues in published content](#other-clues-in-published-content)
      - [Blind guessing](#blind-guessing)
      - [Information obtained through server vulnerabilities and misconfiguration](#information-obtained-through-server-vulnerabilities-and-misconfiguration)
      - [Use of publicly available information](#use-of-publicly-available-information)
      - [File name filter bypass](#file-name-filter-bypass)
  - [Tools](#tools-1)
- [Enumerate Infrastructure and Application Admin Interfaces (OTG-CONFIG-005)](#enumerate-infrastructure-and-application-admin-interfaces--otg-config-005-)
  - [Summary](#summary-1)
  - [How to Test](#how-to-test-4)
    - [Black Box Testing](#black-box-testing-2)
  - [Tools](#tools-2)
- [Test HTTP Methods (OTG-CONFIG-006)](#test-http-methods--otg-config-006-)
  - [Summary](#summary-2)
    - [Arbitrary HTTP Methods](#arbitrary-http-methods)
  - [How to Test](#how-to-test-5)
    - [Discover the Supported Methods](#discover-the-supported-methods)
    - [Test XST Potential](#test-xst-potential)
    - [Testing for arbitrary HTTP methods](#testing-for-arbitrary-http-methods)
    - [Testing for HEAD access control bypass](#testing-for-head-access-control-bypass)
  - [Tools](#tools-3)
- [Test HTTP Strict Transport Security (OTG-CONFIG-007)](#test-http-strict-transport-security--otg-config-007-)
  - [Summary](#summary-3)
  - [How to Test](#how-to-test-6)
- [Test RIA cross domain policy (OTG-CONFIG-008)](#test-ria-cross-domain-policy--otg-config-008-)
  - [Summary](#summary-4)
    - [What are cross-domain policy files?](#what-are-cross-domain-policy-files-)
    - [Crossdomain.xml vs. Clientaccesspolicy.xml](#crossdomainxml-vs-clientaccesspolicyxml)
    - [How can cross domain policy files can be abused?](#how-can-cross-domain-policy-files-can-be-abused-)
    - [Impact of abusing cross-domain access](#impact-of-abusing-cross-domain-access)
  - [How to Test](#how-to-test-7)
    - [Testing for RIA policy files weakness:](#testing-for-ria-policy-files-weakness-)
  - [Tools](#tools-4)

## Test Network/Infrastructure Configuration (OTG-CONFIG-001)

- The following steps need to be taken to test the configuration management infrastructure:

  - The different elements that make up the infrastructure need to be determined in order to understand how they interact with a web application and how they affect its security.
  - All the elements of the infrastructure need to be reviewed in order to make sure that they don’t contain any known vulnerabilities.
  - A review needs to be made of the administrative tools used to maintain all the different elements.
  - The authentication systems, need to reviewed in order to assure that they serve the needs of the application and that they cannot be manipulated by external users to leverage access.
  - A list of defined ports which are required for the application should be maintained and kept under change control.

### How to Test

- Known Server Vulnerabilities
> Some automated tools will flag vulnerabilities based on the web server version retrieved. This leads to both false positives and false negatives. On one hand, if the web server version has been removed or obscured by the local site administrator the scan tool will not flag the server as vulnerable even if it is.

- Administrative tools
  - Determine the mechanisms that control access to these interfaces and their associated susceptibilities. This information may be available online.
  - Change the default username and password.

---

## Test Application Platform Configuration (OTG-CONFIG-002)

### How to Test

#### Black Box Testing

- Sample and known files and directories
- Code Comments review

#### Gray Box Testing

- Configuration review
  - It is impossible to generically say how a server should be configured, however, some common guidelines should be taken into account:
    - Only enable server modules (ISAPI extensions in the case of IIS) that are needed for the application.
    - Handle server errors (40x or 50x) with custom-made pages instead of with the default web server pages.
    - Make sure that the server software runs with minimized privileges in the operating system.
    - Make sure the server software properly logs both legitimate access and errors.
    - Make sure that the server is configured to properly handle overloads and prevent Denial of Service attacks.
    - Never grant non-administrative identities (with the exception of NT SERVICE\WMSvc) access to applicationHost.config, redirection. config, and administration.config (either Read or Write access). This includes Network Service, IIS_IUSRS, IUSR, or any custom identity used by IIS application pools. IIS worker processes are not meant to access any of these files directly.
    - Never share out applicationHost.config, redirection.config, and administration.config on the network.
    - Keep in mind that all users can read .NET Framework machine.config and root web.config files by default. Do not store sensitive information in these files if it should be for administrator eyes only.
    - Encrypt sensitive information that should be read by the IIS worker processes only and not by other users on the machine.
    - Do not grant Write access to the identity that the Web server uses to access the shared applicationHost.config. This identity should have only Read access.
    - Use a separate identity to publish applicationHost.config to the share. Do not use this identity for configuring access to the shared configuration on the Web servers.
    - Use a strong password when exporting the encryption keys for use with shared -configuration.
    - Maintain restricted access to the share containing the shared configuration and encryption keys. If this share is compromised, an attacker will be able to read and write any IIS configuration for your Web servers, redirect traffic from your Web site to malicious sources, and in some cases gain control of all web servers by loading arbitrary code into IIS worker processes.
    - Consider protecting this share with firewall rules and IPsec policies to allow only the member web servers to connect.
- Logging
  - In both cases (server and application logs) several issues should be tested and analysed based on the log contents:
    - Do the logs contain sensitive information?
    - Are the logs stored in a dedicated server?
    - Can log usage generate a Denial of Service condition?
    - How are they rotated? Are logs kept for the sufficient time?
    - How are logs reviewed? Can administrators use these reviews to detect targeted attacks?
    - How are log backups preserved?
    - Is the data being logged data validated (min/max length, chars etc) prior to being logged?
- Sensitive information in logs
  - Event logs will often contain data that is useful to an attacker (information leakage) or can be used directly in exploits:
    - Debug information
    - Stack traces
    - Usernames
    - System component names
    - Internal IP addresses
    - Less sensitive personal data (e.g. email addresses, postal addresses and telephone numbers associated with named individuals)
    - Business data
    - Application source code
    - Session identification values
    - Access tokens
    - Sensitive personal data and some forms of personal identifiable information (PII)
    - Authentication passwords
    - Database connection strings
    - Encryption keys
    - Bank account or payment card holder data
    - Data of a higher security classification than the logging system is allowed to store
    - Commercially-sensitive information
    - Information it is illegal to collect in the relevant jurisdiction
    - Information a user has opted out of collection, or not consented to e.g. use of do not track, or where consent to collect has expired
- Log location
  - it is wiser to keep logs in a separate location and not in the web server itself.
- Log storage
  - Logs can introduce a Denial of Service condition if they are not properly stored. Any attacker with sufficient resources could be able to produce a sufficient number of requests that would fill up the allocated space to log files, if they are not specifically prevented from doing so.
- Log rotation
  - This feature should be tested in order to ensure that:
    - Logs are kept for the time defined in the security policy, not more and not less.
    - Logs are compressed once rotated (this is a convenience, since it will mean that more logs will be stored for the same available disk space).
    - File system permission of rotated log files are the same (or stricter) that those of the log files itself. For example, web servers will need to write to the logs they use but they don’t actually need to write to rotated logs, which means that the permissions of the files can be changed upon rotation to prevent the web server process from modifying these
    - Some servers might rotate logs when they reach a given size. If this happens, it must be ensured that an attacker cannot force logs to rotate in order to hide his tracks.
- Log Access Control
  - Event log information should never be visible to end users. Even web administrators should not be able to see such logs since it breaks separation of duty controls.
- Log review
  - Review of logs can be used for more than extraction of usage statistics of files in the web servers (which is typically what most log-based application will focus on), but also to determine if attacks take place at the web server.
  - In order to analyze web server attacks the error log files of the server need to be analyzed. Review should concentrate on:
    - 40x (not found) error messages. A large amount of these from the same source might be indicative of a CGI scanner tool being used against the web server
    - 50x (server error) messages. These can be an indication of an attacker abusing parts of the application which fail unexpectedly. For example, the first phases of a SQL injection attack will produce these error message when the SQL query is not properly constructed and its execution fails on the back end database. Log statistics or analysis should not be generated, nor stored, in the same server that produces the logs.

---

## Test File Extensions Handling for Sensitive Information (OTG-CONFIG-003)

- Determining how web servers handle requests corresponding to files having different extensions may help in understanding web server behavior depending on the kind of files that are accessed.

### How to Test

- Forced browsing
  - Submit http[s] requests involving different file extensions and verify how they are handled.
  - The verification should be on a per web directory basis. Verify directories that allow script execution.
  - The following file extensions should never be returned by a web server, since they are related to files which may contain sensitive information or to files for which there is no reason to be served.
    - .asa
    - .inc
  - The following file extensions are related to files which, when accessed, are either displayed or downloaded by the browser. Therefore, files with these extensions must be checked to verify that they are indeed supposed to be served (and are not leftovers), and that they do not contain sensitive information.

    - .zip, .tar, .gz, .tgz, .rar, ...: (Compressed) archive files
    - .java: No reason to provide access to Java source files
    - .txt: Text files
    - .pdf: PDF documents
    - .doc, .rtf, .xls, .ppt, ...: Office documents
    - .bak, .old and other extensions indicative of backup files (for example: ~ for Emacs backup files)
- File Upload

    - Windows 8.3 legacy file handling can sometimes be used to defeat file upload filters

### Tools

Vulnerability scanners, such as Nessus and Nikto check for the existence of well-known web directories. They may allow the tester to download the web site structure, which is helpful when trying to determine the configuration of web directories and how individual file extensions are served. Other tools that can be used for this purpose include:

- wget - http://www.gnu.org/software/wget
- curl - http://curl.haxx.se
- google for “web mirroring tools”.

---

## Review Old, Backup and Unreferenced Files for Sensitive Information (OTG-CONFIG-004)

### Summary

While most of the files within a web server are directly handled by the server itself, it isn’t uncommon to find unreferenced or forgotten files that can be used to obtain important information about the infrastructure or the credentials.

Most common scenarios include the presence of renamed old versions of modified files, inclusion files that are loaded into the language of choice and can be downloaded as source, or even automatic or manual backups in form of compressed archives. Backup files can also be generated automatically by the underlying file system the application is hosted on, a feature usually referred to as “snapshots”.

### Threats

Old, backup and unreferenced files present various threats to the security
of a web application:

- Unreferenced files may disclose sensitive information that can facilitate a focused attack against the application; for example include files containing database credentials, configuration files containing references to other hidden content, absolute file paths, etc.
- Unreferenced pages may contain powerful functionality that can be used to attack the application; for example an administration page that is not linked from published content but can be accessed by any user who knows where to find it.
- Old and backup files may contain vulnerabilities that have been fixed in more recent versions; for example viewdoc.old.jsp may contain a directory traversal vulnerability that has been fixed in viewdoc.jsp but can still be exploited by anyone who finds the old version.
- Backup files may disclose the source code for pages designed to execute on the server; for example requesting viewdoc.bak may return the source code for viewdoc.jsp, which can be reviewed for vulnerabilities that may be difficult to find by making blind requests to the executable page. While this threat obviously applies to scripted languages, such as Perl, PHP, ASP, shell scripts, JSP, etc., it is not limited to them, as shown in the example provided in the next bullet.
- Backup archives may contain copies of all files within (or even outside) the webroot. This allows an attacker to quickly enumerate the entire application, including unreferenced pages, source code, include files, etc. For example, if you forget a file named myservlets. jar.old file containing (a backup copy of) your servlet implementation classes, you are exposing a lot of sensitive information which is susceptible to decompilation and reverse engineering.
- In some cases copying or editing a file does not modify the file extension, but modifies the file name. This happens for example in Windows environments, where file copying operations generate file names prefixed with “Copy of “ or localized versions of this string. Since the file extension is left unchanged, this is not a case where an executable file is returned as plain text by the web server, and therefore not a case of source code disclosure. However, these files too are dangerous because there is a chance that they include obsolete and incorrect logic that, when invoked, could trigger application errors, which might yield valuable information to an attacker, if diagnostic message display is enabled.
- Log files may contain sensitive information about the activities of application users, for example sensitive data passed in URL parameters, session IDs, URLs visited (which may disclose additional

### How to Test

#### Black Box Testing

Testing for unreferenced files uses both automated and manual techniques, and typically involves a combination of the following:

##### Inference from the naming scheme used for published content

Enumerate all of the application’s pages and functionality. This can be done manually using a browser, or using an application spidering tool.

Most applications use a recognizable naming scheme, and organize resources into pages and directories using words that describe their function. From the naming scheme used for published content, it is often possible to infer the name and location of unreferenced pages. For example, if a page viewuser.asp is found, then look also for edituser. asp, adduser.asp and deleteuser.asp. If a directory /app/user is found, then look also for /app/admin and /app/manager.

##### Other clues in published content

Many web applications leave clues in published content that can lead to the discovery of hidden pages and functionality. These clues often appear in the source code of HTML and JavaScript files. The source code for all published content should be manually reviewed to identify clues about other pages and functionality. For example:

- Programmers’ comments and commented-out sections of source code may refer to hidden content.
- JavaScript may contain page links that are only rendered within the user’s GUI under certain circumstances
- HTML pages may contain FORMs that have been hidden by disabling the SUBMIT element
- Another source of clues about unreferenced directories is the /robots. txt file used to provide instructions to web robots

##### Blind guessing

In its simplest form, this involves running a list of common file names through a request engine in an attempt to guess files and directories that exist on the server. The following netcat wrapper script will read a wordlist from stdin and perform a basic guessing attack:

```Bash
#!/bin/bash

server=www.targetapp.com
port=80

while read url
do
echo -ne “$url\t”
echo -e “GET /$url HTTP/1.0\nHost: $server\n” | netcat $server
$port | head -1
done | tee outputfile
```

The basic guessing attack should be run against the webroot, and also against all directories that have been identified through other enumeration techniques. More advanced/effective guessing attacks can be performed as follows:

- Identify the file extensions in use within known areas of the application (e.g. jsp, aspx, html), and use a basic wordlist appended with each of these extensions (or use a longer list of common extensions if resources permit).
- For each file identified through other enumeration techniques, create a custom wordlist derived from that filename. Get a list of common file extensions (including ~, bak, txt, src, dev, old, inc, orig, copy, tmp, etc.) and use each extension before, after, and instead of, the extension of the actual file name.

##### Information obtained through server vulnerabilities and misconfiguration

The most obvious way in which a misconfigured server may disclose unreferenced pages is through directory listing. Request all enumerated directories to identify any which provide a directory listing.

##### Use of publicly available information

Pages and functionality in Internet-facing web applications that are not referenced from within the application itself may be referenced from other public domain sources. There are various sources of these references:

- Pages that used to be referenced may still appear in the archives of Internet search engines. For example, 1998results.asp may no longer be linked from a company’s website, but may remain on the server and in search engine databases. This old script may contain vulnerabilities that could be used to compromise the entire site. The site: Google search operator may be used to run a query only against the domain of choice, such as in: site:www.example.com. Using search engines in this way has lead to a broad array of techniques which you may find useful and that are described in the Google Hacking section of this Guide. Check it to hone your testing skills via Google. Backup files are not likely to be referenced by any other files and therefore may have not been indexed by Google, but if they lie in browsable directories the search engine might know about them.
- In addition, Google and Yahoo keep cached versions of pages found by their robots. Even if 1998results.asp has been removed from the target server, a version of its output may still be stored by these search engines. The cached version may contain references to, or clues about, additional hidden content that still remains on the server.
- Content that is not referenced from within a target application may be linked to by third-party websites. For example, an application which processes online payments on behalf of third-party traders may contain a variety of bespoke functionality which can (normally) only be found by following links within the web sites of its customers.

##### File name filter bypass

Because blacklist filters are based on regular expressions, one can sometimes take advantage of obscure OS file name expansion features in which work in ways the developer didn’t expect. The tester can sometimes exploit differences in ways that file names are parsed by the application, web server, and underlying OS and it’s file name conventions.

Example: Windows 8.3 filename expansion “c:\program files” becomes “C:\PROGRA~1”

### Tools

- Vulnerability assessment tools tend to include checks to spot web directories having standard names (such as “admin”, “test”, “backup”, etc.), and to report any web directory which allows indexing. If you can’t get any directory listing, you should try to check for likely backup extensions. Check for example Nessus (http://www.nessus.org), Nikto2(http://www.cirt.net/code/nikto.shtml) or its new derivative Wikto (http://www.sensepost.com/research/wikto/), which also supports Google hacking based strategies.
- Web spider tools: wget (http://www.gnu.org/software/wget/, http://www.interlog.com/~tcharron/wgetwin.html); Sam Spade (http://www.samspade.org); Spike proxy includes a web site crawler function (http://www.immunitysec.com/spikeproxy.html); Xenu (http://home.snafu.de/tilman/xenulink.html); curl (http://curl.haxx.se). Some of them are also included in standard Linux distributions.
- Web development tools usually include facilities to identify broken links and unreferenced files.

---

## Enumerate Infrastructure and Application Admin Interfaces (OTG-CONFIG-005)

### Summary

Administrator interfaces may be present in the application or on the application server to allow certain users to undertake privileged activities on the site. Tests should be undertaken to reveal if and how this privileged functionality can be accessed by an unauthorized or
standard user.

An application may require an administrator interface to enable a privileged user to access functionality that may make changes to how the site functions. Such changes may include:

- user account provisioning
- site design and layout
- data manipulation
- configuration changes

In many instances, such interfaces do not have sufficient controls to protect them from unauthorized access. Testing is aimed at discovering these administrator interfaces and accessing functionality intended for the privileged users.

### How to Test

#### Black Box Testing

The following section describes vectors that may be used to test for the presence of administrative interfaces. These techniques may also be used to test for related issues including privilege escalation, and are described elsewhere in this guide(for example Testing for bypassing authorization schema (OTG-AUTHZ-002) and Testing for Insecure Direct Object References (OTG-AUTHZ-004) in greater detail.

- Directory and file enumeration. An administrative interface may be present but not visibly available to the tester. Attempting to guess the path of the administrative interface may be as simple as requesting: /admin or /administrator etc.. or in some scenarios can be revealed within seconds using Google dorks.
- There are many tools available to perform brute forcing of server contents, see the tools section below for more information. * A tester may have to also identify the file name of the administration page. Forcibly browsing to the identified page may provide access to the interface.
- Comments and links in source code. Many sites use common code that is loaded for all site users. By examining all source sent to the client, links to administrator functionality may be discovered and should be investigated.
- Reviewing server and application documentation. If the application server or application is deployed in its default configuration it may be possible to access the administration interface using information described in configuration or help documentation. Default password lists should be consulted if an administrative interface is found and credentials are required.
- Publicly available information. Many applications such as wordpress have default administrative interfaces.
- Alternative server port. Administration interfaces may be seen on a different port on the host than the main application. For example, Apache Tomcat’s Administration interface can often be seen on port 8080.
- Parameter tampering. A GET or POST parameter or a cookie variable may be required to enable the administrator functionality. Clues to this include the presence of hidden fields such as:
`<input type=”hidden” name=”admin” value=”no”>` or in a cookie: `Cookie: session_cookie; useradmin=0`

Once an administrative interface has been discovered, a combination of the above techniques may be used to attempt to bypass authentication.

If this fails, the tester may wish to attempt a brute force attack. In such an instance the tester should be aware of the potential for administrative account lockout if such functionality is present.

### Tools

- Dirbuster This currently inactive OWASP project is still a great tool for brute forcing directories and files on the server.
- THC-HYDRA is a tool that allows brute-forcing of many interfaces, including form-based HTTP authentication.
- A brute forcer is much better when it uses a good dictionary, for example the netsparker dictionary.

---

## Test HTTP Methods (OTG-CONFIG-006)

### Summary

HTTP defines the following eight methods:

- HEAD
- GET
- POST
- PUT
- DELETE
- TRACE
- OPTIONS
- CONNECT

Some of these methods can potentially pose a security risk for a web application, as they allow an attacker to modify the files stored on the web server and, in some scenarios, steal the credentials of legitimate users. More specifically, the methods that should be disabled are the following:

- PUT: This method allows a client to upload new files on the web server. An attacker can exploit it by uploading malicious files (e.g.: an asp file that executes commands by invoking cmd.exe), or by simply using the victim’s server as a file repository.
- DELETE: This method allows a client to delete a file on the web server. An attacker can exploit it as a very simple and direct way to deface a web site or to mount a DoS attack.
- CONNECT: This method could allow a client to use the web server as a proxy.
- TRACE: This method simply echoes back to the client whatever string has been sent to the server, and is used mainly for debugging purposes. This method, originally assumed harmless, can be used to mount an attack known as **Cross Site Tracing**, which has been discovered by Jeremiah Grossman [WH-WhitePaper_XST_ebook](http://www.cgisecurity.com/whitehat-mirror/WH-WhitePaper_XST_ebook.pdf).

If an application needs one or more of these methods, such as REST Web Services (which may require PUT or DELETE), it is important to check that their usage is properly limited to trusted users and safe conditions.

#### Arbitrary HTTP Methods

Arshan Dabirsiaghi [Bypassing_VBAAC_with_HTTP_Verb_Tampering](http://static.swpag.info/download/Bypassing_VBAAC_with_HTTP_Verb_Tampering.pdf) discovered that many web application frameworks allowed well chosen or arbitrary HTTP methods to bypass an environment level access control check:

- Many frameworks and languages treat "HEAD" as a "GET" request, albeit one without any body in the response. If a security constraint was set on "GET" requests such that only "authenticatedUsers" could access GET requests for a particular servlet or resource, it would be bypassed for the "HEAD" version. This allowed unauthorized blind submission of any privileged GET request.
- Some frameworks allowed arbitrary HTTP methods such as "JEFF" or "CATS" to be used without limitation. These were treated as if a "GET" method was issued, and were found not to be subject to method role based access control checks on a number of languages and frameworks, again allowing unauthorized blind submission of privileged GET requests.

In many cases, code which explicitly checked for a "GET" or "POST" method would be safe.

### How to Test

#### Discover the Supported Methods

To perform this test, the tester needs some way to figure out which HTTP methods are supported by the web server that is being examined.

The OPTIONS HTTP method provides the tester with the most direct and effective way to do that.

RFC 2616 states that, "The OPTIONS method represents a request for information about the communication options available on the request/response chain identified by the Request-URI".

The testing method is extremely straightforward and we only need to fire up netcat (or telnet):

```Bash
$ nc www.victim.com 80
OPTIONS / HTTP/1.1
```

The same test can also be executed using nmap and the http-methods NSE script:

```Bash
nmap -p 443 --script http-methods localhost
```

#### Test XST Potential

The TRACE method, while apparently harmless, can be successfully leveraged in some scenarios to steal legitimate users' credentials. This attack technique was discovered by Jeremiah Grossman in 2003, in an attempt to bypass the HTTPOnly tag that Microsoft introduced in Internet Explorer 6 SP1 to protect cookies from being accessed by JavaScript. As a matter of fact, one of the most recurring attack patterns in Cross Site Scripting is to access the document.cookie object and send it to a web server controlled by the attacker so that he or she can hijack the victim's session. Tagging a cookie as httpOnly forbids JavaScript from accessing it, protecting it from being sent to a third party. However, the TRACE method can be used to bypass this protection and access the cookie even in this scenario.

As mentioned before, TRACE simply returns any string that is sent to the web server. In order to verify its presence (or to double-check the results of the OPTIONS request shown above), the tester can proceed as shown in the following example:

```Bash
$ nc www.victim.com 80
TRACE / HTTP/1.1
```

The response body is exactly a copy of our original request, meaning that the target allows this method. Now, where is the danger lurking? If the tester instructs a browser to issue a TRACE request to the web server, and this browser has a cookie for that domain, the cookie will be automatically included in the request headers, and will therefore be echoed back in the resulting response. At that point, the cookie string will be accessible by JavaScript and it will be finally possible to send it to a third party even when the cookie is tagged as httpOnly.

There are multiple ways to make a browser issue a TRACE request, such as the XMLHTTP ActiveX control in Internet Explorer and XMLDOM in Mozilla and Netscape. However, for security reasons the browser is allowed to start a connection only to the domain where the hostile script resides. This is a mitigating factor, as the attacker needs to combine the TRACE method with another vulnerability in order to mount the attack.

An attacker has two ways to successfully launch a Cross Site Tracing attack:

- Leveraging another server-side vulnerability: the attacker injects the hostile JavaScript snippet that contains the TRACE request in the vulnerable application, as in a normal Cross Site Scripting attack
- Leveraging a client-side vulnerability: the attacker creates a malicious website that contains the hostile JavaScript snippet and exploits some cross-domain vulnerability of the browser of the victim, in order to make the JavaScript code successfully perform a connection to the site that supports the TRACE method and that originated the cookie that the attacker is trying to steal.

#### Testing for arbitrary HTTP methods

Find a page to visit that has a security constraint such that it would normally force a 302 redirect to a log in page or forces a log in directly. The test URL in this example works like this, as do many web applications. However, if a tester obtains a "200" response that is not a log in page, it is possible to bypass authentication and thus authorization.

```Bash
$ nc www.example.com 80
JEFF / HTTP/1.1
```

If the framework or firewall or application does not support the "JEFF" method, it should issue an error page (or preferably a 405 Not Allowed or 501 Not implemented error page). If it services the request, it is vulnerable to this issue.

If the tester feels that the system is vulnerable to this issue, they should issue CSRF-like attacks to exploit the issue more fully:

- FOOBAR /admin/createUser.php?member=myAdmin
- JEFF /admin/changePw.php?member=myAdmin&passwd=foo123&confirm=foo123
- CATS /admin/groupEdit.php?group=Admins&member=myAdmin&action=add

With some luck, using the above three commands - modified to suit the application under test and testing requirements - a new user would be created, a password assigned, and made an administrator.

#### Testing for HEAD access control bypass

Find a page to visit that has a security constraint such that it would normally force a 302 redirect to a log in page or forces a log in directly. The test URL in this example works like this, as do many web applications. However, if the tester obtains a "200" response that is not a login page, it is possible to bypass authentication and thus authorization.

```Bash
$ nc www.example.com 80
HEAD /admin HTTP/1.1

```

If the tester gets a "405 Method not allowed" or "501 Method Unimplemented", the target (application/framework/language/system/firewall) is working correctly. If a "200" response code comes back, and the response contains no body, it's likely that the application has processed the request without authentication or authorization and further testing is warranted.

If the tester thinks that the system is vulnerable to this issue, they should issue CSRF-like attacks to exploit the issue more fully:

- HEAD /admin/createUser.php?member=myAdmin
- HEAD /admin/changePw.php?member=myAdmin&passwd=foo123&confirm=foo123
- HEAD /admin/groupEdit.php?group=Admins&member=myAdmin&action=add

With some luck, using the above three commands - modified to suit the application under test and testing requirements - a new user would be created, a password assigned, and made an administrator, all using blind request submission.

### Tools

- NetCat - http://nc110.sourceforge.net
- cURL - http://curl.haxx.se/

---

## Test HTTP Strict Transport Security (OTG-CONFIG-007)

### Summary

The HTTP Strict Transport Security (HSTS) header is a mechanism that web sites have to communicate to the web browsers that all traffic exchanged with a given domain must always be sent over https, this will help protect the information from being passed over unencrypted requests.

Considering the importance of this security measure it is important to verify that the web site is using this HTTP header, in order to ensure that all the data travels encrypted from the web browser to the server.

The **HTTP Strict Transport Security (HSTS)** feature lets a web application to inform the browser, through the use of a special response header, that it should never establish a connection to the the specified domain servers using HTTP. Instead it should automatically establish all connection requests to access the site through HTTPS.

The HTTP strict transport security header uses two directives:

- max-age: to indicate the number of seconds that the browser should automatically convert all HTTP requests to HTTPS.
- includeSubDomains: to indicate that all web application’s sub-domains must use HTTPS.

Here's an example of the HSTS header implementation:
`Strict-Transport-Security: max-age=60000; includeSubDomains`

The use of this header by web applications must be checked to find if the following security issues could be produced:

- Attackers sniffing the network traffic and accessing the information transferred through an unencrypted channel.
- Attackers exploiting a man in the middle attack because of the problem of accepting certificates that are not trusted.
- Users who mistakenly entered an address in the browser putting HTTP instead of HTTPS, or users who click on a link in a web application which mistakenly indicated the http protocol.

### How to Test

Testing for the presence of HSTS header can be done by checking for the existence of the HSTS header in the server's response in an interception proxy, or by using curl as follows:

```Bash
curl -s -D- https://domain.com/ | grep Strict
```

Result expected:

   `Strict-Transport-Security: max-age=...`

---

## Test RIA cross domain policy (OTG-CONFIG-008)

### Summary

Rich Internet Applications (RIA) have adopted Adobe's crossdomain.xml policy files to allow for controlled cross domain access to data and service consumption using technologies such as Oracle Java, Silverlight, and Adobe Flash. Therefore, a domain can grant remote access to its services from a different domain. However, often the policy files that describe the access restrictions are poorly configured. Poor configuration of the policy files enables Cross-site Request Forgery attacks, and may allow third parties to access sensitive data meant for the user.

#### What are cross-domain policy files?

A cross-domain policy file specifies the permissions that a web client such as Java, Adobe Flash, Adobe Reader, etc. use to access data across different domains. For Silverlight, Microsoft adopted a subset of the Adobe's crossdomain.xml, and additionally created it's own cross-domain policy file: clientaccesspolicy.xml.

Whenever a web client detects that a resource has to be requested from other domain, it will first look for a policy file in the target domain to determine if performing cross-domain requests, including headers, and socket-based connections are allowed.

Master policy files are located at the domain's root. A client may be instructed to load a different policy file but it will always check the master policy file first to ensure that the master policy file permits the requested policy file.

#### Crossdomain.xml vs. Clientaccesspolicy.xml

Most RIA applications support crossdomain.xml. However in the case of Silverlight, it will only work if the crossdomain.xml specifies that access is allowed from any domain. For more granular control with Silverlight, clientaccesspolicy.xml must be used.

Policy files grant several types of permissions:

- Accepted policy files (Master policy files can disable or restrict specific policy files)
- Sockets permissions
- Header permissions
- HTTP/HTTPS access permissions
- Allowing access based on cryptographic credentials

An example of an overly permissive policy file:

```Xml
<?xml version="1.0"?>
<!DOCTYPE cross-domain-policy SYSTEM
"http://www.adobe.com/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy>
   <site-control permitted-cross-domain-policies="all"/>
   <allow-access-from domain="*" secure="false"/>
   <allow-http-request-headers-from domain="*" headers="*" secure="false"/>
</cross-domain-policy>
```

#### How can cross domain policy files can be abused?

- Overly permissive cross-domain policies.
- Generating server responses that may be treated as cross-domain policy files.
- Using file upload functionality to upload files that may be treated as cross-domain policy files.

#### Impact of abusing cross-domain access

- Defeat CSRF protections.
- Read data restricted or otherwise protected by cross-origin policies.

### How to Test

#### Testing for RIA policy files weakness:

To test for RIA policy file weakness the tester should try to retrieve the policy files crossdomain.xml and clientaccesspolicy.xml from the application's root, and from every folder found.

For example, if the application's URL is http://www.owasp.org, the tester should try to download the files http://www.owasp.org/crossdomain.xml and http://www.owasp.org/clientaccesspolicy.xml.

After retrieving all the policy files, the permissions allowed should be be checked under the least privilege principle. Requests should only come from the domains, ports, or protocols that are necessary. Overly permissive policies should be avoided. Policies with "*" in them should be closely examined.

Example:

```Xml
<cross-domain-policy>
 <allow-access-from domain="*" />
</cross-domain-policy>
```

Result Expected:

- A list of policy files found.
- A list of weak settings in the policies.

### Tools

- Nikto
- OWASP Zed Attack Proxy Project
- W3af
