# Information Gathering (OWASP Guide)

<!-- TOC -->

- [Conduct search engine discovery/reconnaissance for information leakage (OTG-INFO-001)](#conduct-search-engine-discoveryreconnaissance-for-information-leakage-otg-info-001)
  - [Test Objectives](#test-objectives)
  - [How to Test](#how-to-test)
    - [Use a search engine to search for](#use-a-search-engine-to-search-for)
    - [Google Hacking Database](#google-hacking-database)
  - [Tools](#tools)
- [Fingerprint Web Server (OTG-INFO-002)](#fingerprint-web-server-otg-info-002)
  - [Test Objectives](#test-objectives-1)
  - [How to Test](#how-to-test-1)
    - [Black Box testing](#black-box-testing)
    - [Protocol Behavior](#protocol-behavior)
  - [Tools](#tools-1)
- [Review Webserver Metafiles for Information Leakage (OTG-INFO-003)](#review-webserver-metafiles-for-information-leakage-otg-info-003)
  - [Test Objectives](#test-objectives-2)
  - [How to Test](#how-to-test-2)
    - [robots.txt](#robotstxt)
  - [Tools](#tools-2)
- [Enumerate Applications on Webserver (OTG-INFO-004)](#enumerate-applications-on-webserver-otg-info-004)
  - [Test Objectives](#test-objectives-3)
  - [How to Test](#how-to-test-3)
    - [1. Different base URL](#1-different-base-url)
    - [2. Non-standard ports](#2-non-standard-ports)
    - [3. Virtual hosts](#3-virtual-hosts)
  - [Tools](#tools-3)
- [Review webpage comments and metadata for information leakage (OTG-INFO-005)](#review-webpage-comments-and-metadata-for-information-leakage-otg-info-005)
  - [Test Objectives](#test-objectives-4)
  - [Tools](#tools-4)
- [Identify application entry points (OTG-INFO-006)](#identify-application-entry-points-otg-info-006)
  - [Test Objectives](#test-objectives-5)
  - [How to Test](#how-to-test-4)
  - [Tools](#tools-5)
- [Map execution paths through application (OTG-INFO-007)](#map-execution-paths-through-application-otg-info-007)
  - [Test Objectives](#test-objectives-6)
  - [How to Test](#how-to-test-5)
    - [Black Box Testing](#black-box-testing)
    - [Gray/White Box testing](#graywhite-box-testing)
  - [Tools](#tools-6)
- [Fingerprint Web Application Framework (OTG-INFO-008)](#fingerprint-web-application-framework-otg-info-008)
  - [Test Objectives](#test-objectives-7)
  - [How to Test](#how-to-test-6)
    - [Black Box testing](#black-box-testing-1)
  - [Tools](#tools-7)
- [Fingerprint Web Application (OTG-INFO-009)](#fingerprint-web-application-otg-info-009)
  - [Test Objectives](#test-objectives-8)
  - [Tools](#tools-8)
- [Map Application Architecture (OTG-INFO-010)](#map-application-architecture-otg-info-010)
  - [Test Objectives](#test-objectives-9)
- [Map Application Architecture (OTG-INFO-010)](#map-application-architecture-otg-info-010-1)
  - [Test Objectives](#test-objectives-10)

<!-- /TOC -->

## Conduct search engine discovery/reconnaissance for information leakage (OTG-INFO-001)

### Test Objectives

 To understand what sensitive design and configuration information of the application/system/organization is exposed both directly (on the organization’s website) or indirectly (on a third party website).

### How to Test

#### Use a search engine to search for

- Network diagrams and configurations
- Archived posts and emails by administrators and other key staff
- Log on procedures and username formats
- Usernames and passwords
- Error message content
- Development, test, UAT and staging versions of the website

#### Google Hacking Database

The Google Hacking Database is list of useful search queries for Google.

- Queries are put in several categories:
  - Footholds
  - Files containing usernames
  - Sensitive Directories
  - Web Server Detection
  - Vulnerable Files
  - Vulnerable Servers
  - Error Messages
  - Files containing juicy info
  - Files containing passwords
  - Sensitive Online Shopping Info

### Tools

- [punk spider](http://punkspider.hyperiongray.com/)
- [FoundStone SiteDigger](http://www.mcafee.com/uk/downloads/free-tools/sitedigger.aspx)
- [Google Hacker](http://yehg.net/lab/pr0js/files.php/googlehacker.zip)
- [Stach & Liu’s Google Hacking Diggity Project](http://www.stachliu.com/resources/tools/google-hacking-diggity-project/)

---

## Fingerprint Web Server (OTG-INFO-002)

### Test Objectives

Find the version and type of a running web server to determine known vulnerabilities and the appropriate exploits to use during testing.

### How to Test

#### Black Box testing

The simplest and most basic form of identifying a web server is to look at the Server field in the HTTP response header.

Netcat is used in this experiment.

```Bash
$ nc 202.41.76.251 80
HEAD / HTTP/1.0
```

#### Protocol Behavior

More refined techniques take in consideration various characteristics of the several web servers available on the market. Below is a list of some methodologies that allow testers to deduce the type of web server in use.

##### HTTP header field ordering

The first method consists of observing the ordering of the several headers in the response. Every web server has an inner ordering of the header.

We will use Netcat also to see response headers

```Bash
$ nc apache.example.com 80
HEAD / HTTP/1.0
```

##### Malformed requests test

Another useful test to execute involves sending malformed requests or requests of nonexistent pages to the server. Consider the following HTTP responses.

```Bash
$ nc apache.example.com 80
GET / HTTP/3.0
```

```Bash
$ nc apache.example.com 80
GET / JUNK/1.0
```

##### Automated Testing

Rather than rely on **manual banner grabbing** and analysis of the web server headers, a tester can use automated tools to achieve the same results.

There are many tests to carry out in order to accurately fingerprint a web server. Luckily, there are tools that automate these tests.

“httprint” is one of such tools. httprint uses a signature dictionary that allows

### Tools

- [httprint](http://net-square.com/httprint.html)
- [httprecon](http://www.computec.ch/projekte/httprecon/)
- [Netcraft](http://www.netcraft.com)
- [Desenmascarame](http://desenmascara.me)

---

## Review Webserver Metafiles for Information Leakage (OTG-INFO-003)

### Test Objectives

1. Information leakage of the web application’s directory or folder path(s).
1. Create the list of directories that are to be avoided by Spiders, Robots, or Crawlers.

### How to Test

#### robots.txt

Web Spiders, Robots, or Crawlers retrieve a web page and then recursively
traverse hyperlinks to retrieve further web content. Their accepted behavior is specified by the Robots Exclusion Protocol of the robots.txt file in the web root directory.

##### robots.txt in webroot - with “wget” or “curl”

`$ wget http://www.google.com/robots.txt`

`$ curl -O http://www.google.com/robots.txt`

##### robots.txt in webroot - with rockspider

“rockspider” automates the creation of the initial scope for Spiders/Robots/Crawlers of files and directories/folders of a web site.

For example, to create the initial scope based on the Allowed: directive
from www.google.com using “rockspider”:

`$ ./rockspider.pl -www www.google.com`

##### Analyze robots.txt using Google Webmaster Tools

Web site owners can use the Google “Analyze robots.txt” function to analyse the website as part of its “Google Webmaster Tools” (https://www.google.com/webmasters/tools). This tool can assist with testing
and the procedure is as follows:

1. Sign into Google Webmaster Tools with a Google account.
1. On the dashboard, write the URL for the site to be analyzed.
1. Choose between the available methods and follow the on screen instruction.

##### META Tag

If there is no “<META NAME=”ROBOTS” ... >” entry then the “Robots Exclusion Protocol” defaults to “INDEX,FOLLOW” respectively. Therefore, the other two valid entries defined by the “Robots Exclusion Protocol” are prefixed with “NO...” i.e. “NOINDEX” and “NOFOLLOW”.

Web spiders/robots/crawlers can intentionally ignore the “<META NAME=”ROBOTS”” tag as the robots.txt file convention is preferred.

Hence, **<META> Tags should not be considered the primary mechanism, rather a complementary control to robots.txt**.

##### Exploring \<META\> Tags - with Burp

Based on the Disallow directive(s) listed within the robots.txt file in webroot:

- regular expression search for `“<META NAME=”ROBOTS”`” within each web page is undertaken and the result compared to the robots.txt file in webroot.

### Tools

- Browser (View Source function)
- curl
- wget
- rockspider

---

## Enumerate Applications on Webserver (OTG-INFO-004)

### Test Objectives

Enumerate the applications within scope that exist on a web server

### How to Test

There are three factors influencing how many applications are related to a given DNS name (or an IP address):

#### 1. Different base URL

For example, the same symbolic name may be associated to three web applications such as: http://www.example.com/url1 http://www.example.com/url2 http://www.example.com/url3

##### Approaches to address issue 1 - non-standard URLs

There is no way to fully ascertain the existence of non-standardnamed web applications.

First, if the web server is mis-configured and allows directory browsing, it may be possible to spot these applications. Vulnerability scanners may help in this respect.

Second, A __query for__ `site: www.example.com` might help. Among the returned URLs there could be one pointing to such a non-obvious application.

Another option is to probe for URLs which might be likely candidates for non-published applications. For example, a web mail front end might be accessible from URLs such as https://www.example.com/webmail, https://webmail.example.com/, or https://mail.example.com/. The same holds for administrative interfaces. So doing a bit of dictionary-style searching (or “intelligent guessing”) could yield some results. Vulnerability scanners may help in this respect.

#### 2. Non-standard ports

Web applications may be associated with arbitrary TCP ports, and can be referenced by specifying the port number as follows: http[s]://www.example.com:port/. For example http://www.example.com:20000/.

##### Approaches to address issue 2 - non-standard ports

It is easy to check for the existence of web applications on non-standard ports.

A port scanner such as nmap is capable of performing service recognition by means of the -sV option, and will identify http services on arbitrary ports. What is required is a full scan of the whole 64k TCP port address space.

For example, the following command will look up, with a TCP connect scan, all open ports on IP 192.168.1.100:

`nmap –PN –sT –sV –p0-65535 192.168.1.100`

#### 3. Virtual hosts

DNS allows a single IP address to be associated with one or more symbolic names. For example, the IP address 192.168.1.100 might be associated to DNS names www.example.com, helpdesk.example.com, webmail.example.com.

It is not necessary that all the names belong to the same DNS domain. This 1-to-N relationship may be reflected to serve different content by using so called virtual hosts. The information specifying the virtual host we are referring to is embedded in the HTTP 1.1 Host: header.

One would not suspect the existence of other web applications in addition to the obvious www.example.com, unless they know of helpdesk. example.com and webmail.example.com.

##### Approaches to address issue 3 - virtual hosts

There are a number of techniques which may be used to identify DNS names associated to a given IP address x.y.z.t.

###### 1. DNS zone transfers

This technique has limited use nowadays, given the fact that zone transfers are largely not honored by DNS servers. However, it may be worth a try.

 First of all, testers must determine the name servers serving x.y.z.t. If a symbolic name is known for x.y.z.t (let it be www.example.com), its name servers can be determined by means of tools such as nslookup, host, or dig, by requesting DNS NS records.

If no symbolic names are known for x.y.z.t, but the target definition contains at least a symbolic name, testers may try to apply the same process and query the name server of that name (hoping that x.y.z.t will be served as well by that name server). For example, if the target consists of the IP address x.y.z.t and the name mail.example.com, determine the name servers for domain example.com.

The following example shows how to identify the name servers for www.owasp.org by using the host command:

`$ host -t ns www.owasp.org`

A zone transfer may now be requested to the name servers for domain example.com. If the tester is lucky, they will get back a list of the DNS entries for this domain. This will include the obvious www.example.com and the not-so-obvious helpdesk.example.com and webmail.example.com (and possibly others). Check all names returned by the zone transfer and consider all of those which are related to the target being evaluated.
Trying to request a zone transfer for owasp.org from one of its name servers:

`$ host -l www.owasp.org ns1.secure.net`

###### 2. DNS inverse queries

This process is similar to the previous one, but relies on inverse (PTR) DNS records. Rather than requesting a zone transfer, try setting the record type to PTR and issue a query on the given IP address. If the testers are lucky, they may get back a DNS name entry. This technique relies on the existence of IP-to-symbolic name maps, which is not guaranteed.

###### 3. Web-based DNS searches

This kind of search is akin to DNS zone transfer, but relies on webbased services that enable name-based searches on DNS. One such service is the Netcraft Search DNS service, available at [searchdns.netcraft.com/?host](http://searchdns.netcraft.com/?host) The tester may query for a list of names belonging to your domain of choice, such as example.com. Then they will check whether the names they obtained are pertinent to the target they are examining.

###### 3. Reverse-IP services

Reverse-IP services are similar to DNS inverse queries, with the difference that the testers query a web-based application instead of a name server. There are a number of such services available. Since they tend to return partial (and often different) results, it is better to use
multiple services to obtain a more comprehensive analysis.

- Domain tools reverse IP: http://www.domaintools.com/reverse-ip/ (requires free membership)
- MSN search: http://search.msn.com syntax: “ip:x.x.x.x” (without the quotes)
- Webhosting info: http://whois.webhosting.info/ syntax: http://whois.webhosting.info/x.x.x.x
- DNSstuff: http://www.dnsstuff.com/ (multiple services available)
- http://www.net-square.com/mspawn.html (multiple queries on
- domains and IP addresses, requires installation)
- tomDNS: http://www.tomdns.net/index.php (some services are still private at the time of writing)
- SEOlogs.com: http://www.seologs.com/ip-domains.html (reverse-IP/domain lookup)

### Tools

- examining the result of a query for “site: www.example.com”.
- scan all ports and get finger prints `nmap –PN –sT –sV –p0-65535 192.168.1.100`
- identify the name servers for www.owasp.org by using the host command `$ host -t ns www.owasp.org`
- netcraft Search DNS service, available at http:// searchdns.netcraft.com/?host
- Domain tools reverse IP: http://www.domaintools.com/reverse-ip/ (requires free membership)
- MSN search: http://search.msn.com syntax: “ip:x.x.x.x” (without the quotes)
- Webhosting info: http://whois.webhosting.info/ syntax: http:// whois.webhosting.info/x.x.x.x
- DNSstuff: http://www.dnsstuff.com/ (multiple services available)
- http://www.net-square.com/mspawn.html (multiple queries on domains and IP addresses, requires installation)
- tomDNS: http://www.tomdns.net/index.php (some services are still private at the time of writing)
- SEOlogs.com: http://www.seologs.com/ip-domains.html (reverse-IP/domain lookup)
  - DNS lookup tools such as nslookup, dig and similar.
- Search engines (Google, Bing and other major search engines).
- Specialized DNS-related web-based search service: see text.
- Nmap - http://www.insecure.org
- Nessus Vulnerability Scanner - http://www.nessus.org
- Nikto - http://www.cirt.net/nikto2

---

## Review webpage comments and metadata for information leakage (OTG-INFO-005)

### Test Objectives

Review webpage comments and metadata to better understand the application and to find any information leakage.

### Tools

- Wget
- Browser “view source” function
- Eyeballs
- Curl

---

## Identify application entry points (OTG-INFO-006)

### Test Objectives

Understand how requests are formed and typical responses from the application.

### How to Test

Before any testing begins, the tester should always get a good understanding of the application and how the user and browser communicates with it.

As the tester walks through the application, they should pay special attention to all HTTP requests (GET and POST Methods, also known as Verbs), as well as every parameter and form field that is passed to the application. In addition, they should pay attention to when GET requests are used and when POST requests are used to pass parameters to the application. It is very common that GET requests are used, but when sensitive information is passed, it is often done within the body of a POST request.

Note that to see the parameters sent in a POST request, the tester will need to use a tool such as an intercepting proxy (for example, OWASP: Zed Attack Proxy (ZAP)) or a browser plug-in. Within the POST request, the tester should also make special note of any hidden form fields that are being passed to the application, as these usually contain sensitive information, such as state information, quantity of items, the price of items, that the developer never intended for you to see or change.

Below are some points of interests for all requests and responses. Within the requests section, focus on the GET and POST methods, as these appear the majority of the requests. Note that other methods, such as PUT and DELETE, can be used. Often, these more rare requests, if allowed, can expose vulnerabilities. There is a special section in this guide dedicated for testing these HTTP methods.

Requests:

- Identify where GETs are used and where POSTs are used.
- Identify all parameters used in a POST request (these are in the body of the request).
- Within the POST request, pay special attention to any hidden parameters. When a POST is sent all the form fields (including hidden parameters) will be sent in the body of the HTTP message to the application. These typically aren’t seen unless a proxy or view the HTML source code is used. In addition, the next page shown, its data, and the level of access can all be different depending on the value of the hidden parameter(s).
- Identify all parameters used in a GET request (i.e., URL), in particular the query string (usually after a ? mark).
- Identify all the parameters of the query string. These usually are in a pair format, such as foo=bar. Also note that many parameters can be in one query string such as separated by a &, ~, :, or any other special character or encoding.
- A special note when it comes to identifying multiple parameters in one string or within a POST request is that some or all of the parameters will be needed to execute the attacks. The tester needs to identify all of the parameters (even if encoded or encrypted) and identify which ones are processed by the application. Later sections of the guide will identify how to test these parameters. At this point, just make sure each one of them is identified.
- Also pay attention to any additional or custom type headers not typically seen (such as debug=False).

Responses:

• Identify where new cookies are set (Set-Cookie header), modified, or added to.
• Identify where there are any redirects (3xx HTTP status code), 400 status codes, in particular 403 Forbidden, and 500 internal server errors during normal responses (i.e., unmodified requests).
• Also note where any interesting headers are used. For example, “Server: BIG-IP” indicates that the site is load balanced. Thus, if a site is load balanced and one server is incorrectly configured, then the tester might have to make multiple requests to access the vulnerable server, depending on the type of load balancing used.


### Tools

- Tools
- Intercepting Proxy:
  - OWASP: Zed Attack Proxy (ZAP)
  - OWASP: WebScarab
  - Burp Suite
  - CAT
- Browser Plug-in:
  - TamperIE for Internet Explorer
  - Tamper Data for Firefox

---

## Map execution paths through application (OTG-INFO-007)

### Test Objectives

- Map the target application and understand the principal workflows.

Without a thorough understanding of the layout of the application, it is unlkely that it will be tested thoroughly.

### How to Test

In black box testing it is extremely difficult to test the entire code base. Not just because the tester has no view of the code paths through the application, but even if they did, to test all code paths would be very time consuming.

One way to reconcile this is to document what code paths were discovered and tested.

There are several ways to approach the testing and measurement of code coverage:

- Path - test each of the paths through an application that includes combinatorial and boundary value analysis testing for each decision path. While this approach offers thoroughness, the number of testable paths grows exponentially with each decision branch.

- Data flow (or taint analysis) - tests the assignment of variables via external interaction (normally users). Focuses on mapping the flow, transformation and use of data throughout an application.
- Race - tests multiple concurrent instances of the application manipulating the same data.

The trade off as to what method is used and to what degree each method is used should be negotiated with the application owner. Simpler approaches could also be adopted, including asking the application owner what functions or code sections they are particularly concerned about and how those code segments can be reached.

#### Black Box Testing

To demonstrate code coverage to the application owner, the tester can start with a spreadsheet and document all the links discovered by spidering the application (either manually or automatically). Then the tester can look more closely at decision points in the application and investigate how many significant code paths are discovered.

These should then be documented in the spreadsheet with URLs, prose and screenshot descriptions of the paths discovered.

#### Gray/White Box testing

Ensuring sufficient code coverage for the application owner is far easier with the gray and white box approach to testing. Information solicited by and provided to the tester will ensure the minimum requirements for code coverage are met.

### Tools

- Zed Attack Proxy (ZAP)
  - ZAP offers the following automatic spidering features:
    - Spider Site
    - Spider Subtree
    - Spider URL
    - Spider all in Scope
- List of spreadsheet software
- Diagramming software

---

## Fingerprint Web Application Framework (OTG-INFO-008)

### Test Objectives

To define type of used web framework so as to have a better understanding of the security testing methodology.

### How to Test

#### Black Box testing

There are several most common locations to look in in order to define the current framework:

- HTTP headers
- Cookies
- HTML source code
- Specific files and folders

##### HTTP headers

The most basic form of identifying a web framework is to look at the X-Powered-By field in the HTTP response header. Many tools can be used to fingerprint a target. The simplest one is netcat utility.


```Bash
$ nc 127.0.0.1 80
HEAD / HTTP/1.0
```

##### Cookies

Another similar and somehow more reliable way to determine the current web framework are framework-specific cookies.


### Tools

- WhatWeb Website: http://www.morningstarsecurity.com/research/whatweb Currently one of the best fingerprinting tools on the market. Included in a default Kali Linux build.
- BlindElephant Website: https://community.qualys.com/community/blindelephant This great tool works on the principle of static file checksum based version difference thus providing a very high quality of fingerprinting.
- Wappalyzer Website: http://wappalyzer.com Wapplyzer is a Firefox Chrome plug-in. It works only on regular expression matching and doesn’t need anything other than the page to be loaded on browser. It works completely at the browser level and gives results in the form of icons. Although sometimes it has false positives, this is very handy to have notion of what technologies were used to construct a target website immediately after browsing a page.

---

## Fingerprint Web Application (OTG-INFO-009)

### Test Objectives

Identify the web application and version to determine known vulnerabilities and the appropriate exploits to use during testing.

### Tools

- FuzzDB wordlists of predictable files/folders (http://code.google.com/p/fuzzdb/).
- WhatWeb Website: http://www.morningstarsecurity.com/research/whatweb
- BlindElephant Website: https://community.qualys.com/community/blindelephant
- Wappalyzer Website: http://wappalyzer.com

---

## Map Application Architecture (OTG-INFO-010)

### Test Objectives

Determine firewalls, load balancers, proxies, databases,...

---

## Map Application Architecture (OTG-INFO-010)

### Test Objectives

Before performing an in-depth review it is necessary to map the network and application architecture. The different elements that make up the infrastructure need to be determined to understand how they interact with a web application and how they affect security. We need to know which server types, databases, firewalls, load balancers, .... are being used in the web app.
