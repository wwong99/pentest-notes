# Passive information gathering
1. ### Google
	- use search terms like: insite, intitle, intext, .
	- Check Google dorks [Google dorks](https://www.exploit-db.com/google-hacking-database/)

2. ### Email Harvesting
	- Use shell command

		```shell
		theharvester -d target.com -b google >target_google.txt
		theharvester -d target.com -l 10 -b bing >target_bing.txt
		```

3. ### Netcraft
	- [netcraft](http://www.netcraft.com/)
	- [search dns](http://searchdns.netcraft.com/)
	- [Search Engine Features Chart](http://www.searchengineshowdown.com/features/)

4. ### Whois

	```Bash
	Whois target.com
	whois 10.10.10.10
	```

5. ### Recon-ng
	- We’ll start by using the whois_poc module to come up with employee names and email addresses

		```Bash
		root@kali:~# recon-ng
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
