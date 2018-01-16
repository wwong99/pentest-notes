# OSINT By recon-ng

## Study case (trivago.com)

```Bash
> recon-ng

## now let's add a workspace
> workspaces add trivago.com

## Add the target domain
> add domains trivago.com

## Double check if domain is added
> show domains

## find related hosts to our domain
> load netcraft
> run

## check added hosts
> show hosts

## Searching web
> load google
> load google_site_web
> run

## Now it's time for brute-forcing
> load brute
> load brute_hosts
> run

## resolve hosts
> load resolve
> run

## now reverse resolve
> load reverse_resolve
> use recon/hosts-hosts/reverse_resolve
> run

## check hosts
> show hosts

## Now let's get some geolocation info
> load ipinfodb
> run

## more geolocation info

### first edit /usr/local/Cellar/recon-ng/4.9.2/libexec/modules/recon/locations-locations/geocode.py
### also edit /usr/local/Cellar/recon-ng/4.9.2/libexec/modules/recon/locations-locations/reverse_geocode.py
### line 21  instead of `return` make it `continue`

> load geocode
> use recon/locations-locations/geocode

> show options
> show info
> set SOURCE query SELECT DISTINCT host FROM hosts WHERE host IS NOT NULL
> run

## Check locations
> show locations

## Now reverse
> load reverse
> use recon/locations-locations/reverse_geocode
> run

## Check locations
> show locations

## Now let's change reverse_geocode query to run on hosts table
> show info
> set SOURCE query SELECT DISTINCT latitude || ',' || longitude FROM hosts WHERE latitude IS NOT NULL AND longitude IS NOT NULL
> run

## Check locations
> show locations

## now let's search contacts
> search contacts
> use recon/domains-contacts/whois_pocs
> run

> load pgp_search
> run

## After you found some contacts, now let's see if there is any leaks for them
> use recon/contacts-credentials/hibp_paste
> run

## Now let's find some interesting files on the servers
> use discovery/info_disclosure/interesting_files
> run

```

https://github.com/jhaddix/domain
