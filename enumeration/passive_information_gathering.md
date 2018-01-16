# Passive information gathering

<!-- TOC -->

- [Google](#google)
- [Email Harvesting](#email-harvesting)
- [Netcraft](#netcraft)
- [Whois](#whois)
- [Recon-ng](#recon-ng)
- [Search for people](#search-for-people)
- [Search Engine Recon Defenses](#search-engine-recon-defenses)

<!-- /TOC -->

## Google

- use search terms like: insite, intitle, intext, .
- Check Google dorks [Google dorks](https://www.exploit-db.com/google-hacking-database/)

## Email Harvesting

- Use shell command

```Bash
> theharvester -d target.com -b google >target_google.txt
> theharvester -d target.com -l 10 -b bing >target_bing.txt
```

## Netcraft

- [netcraft](http://www.netcraft.com/)
- [search dns](http://searchdns.netcraft.com/)
- [Search Engine Features Chart](http://www.searchengineshowdown.com/features/)

## Whois

- Whois databases contain a treasure trove of information Many can be accessed via the web
  - Alternatively, use the `whois` command built into many UNIX implementations
  - Used to gather contact names, DNS information, and other data
- First, look up the target at InterNIC to determine the registrar
  - https://www.internic.net/whois.html
  - Operated by Internet Corporation for Assigned Names and Numbers (ICANN)
- Then, go to registrar’s whois database to get detailed records
  - For example, https://www.networksolutions.com/whois/index.jsp

- Attackers look for IP address assignments in these geographic whois databases:
  - MUN (American Registry for Internet Numbers)
    -http://www.arin.net
  - RIPE NCC (Reseaux IP Europeens Network Coordination Centre)
    -http://www.ripe.net
  - APNIC (Asia Pacific Network Information Centre)
    -http://www.apnic.net
  - LACNIC (Latin American and Caribbean NIC)
    - http://lacnic.net
  - AFRINIC (Africa’s NIC)
    - http://www.afrinic.net
  - DoDNIC (Department of Defense NIC)
    - http://www.nic.mil (requires account and certificate)

- Another useful site to check out for Whois information
  - http://www.uwhois.com with over 246 countries

```Bash
> Whois target.com
> whois 10.10.10.10
```

## Recon-ng

Check [here](osint_recon_ng.md) for more detat

- We’ll start by using the whois_poc module to come up with employee names and email addresses

```Bash
> recon-ng
[recon-ng][default] > use recon/contacts/gather/http/api/whois_pocs
```

- Next, we can use recon-ng to search sources such as xssed for existing XSS vulnerabilities that have been reported, but not yet fixed

```Bash
recon-ng > use recon/hosts/enum/http/web/xssed
```

- We can also use the google_site module to search for additional target.com subdomains, via the Google search engine

```Bash
recon­-ng > use recon/hosts/gather/http/web/google_site
```

- Another useful example is the ip_neighbour module, which attempts to discover neighbouring IP addresses of the target domain, possibly discovering other domains in the process.

```Bash
recon-ng > use recon/hosts/gather/http/web/ip_neighbor
```

> Many of the modules in recon-ng require API keys with their respective service providers. Take some time to check out recon-ng and its various modules

## Search for people

- You can use http://www.yasni.com/

## Search Engine Recon Defenses

- Look for information leakage using Google yourself
- Remove the website (robots.txt file)
  - robots.txt is NOT a security feature; it must be world readable for the search engine crawlers to find it
  - It draws attention to files, and careful attackers are wise to pktnder it for possibly interesting directories and files on a target website
  - Interesting place to refer to a honeypot web page, only referred to in robots.bt
  - Monitor all IP addresses that try to access page
- Remove individual pages ( “NOINDEX, NOFOLLOW’ meta tag)
- Remove snippets ( “NOSNIPPET” meta tag)
- Remove cached pages ( “NOARCHIVE” meta tag)
- Remove an image from Google’s Image Search
- Remove unwanted items from Google
  - URL re-crawl request form (https://www.google.com/webmasters/tools/submit-url)
- See http://www.robotstxt.org/robotstxt.html for info about non-Google crawlers
