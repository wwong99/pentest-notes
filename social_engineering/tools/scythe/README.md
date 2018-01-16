Scythe
======

scythe: account enumerator

    Account Enumerator is designed to make it simple to perform account
    enumeration as part of security testing. The framework offers the ability
    to easily create new modules (XML files) and speed up the process of testing.

    This tool was created with 2 main use cases in mind:

    - The ability to test a range of email addresses across a range of sites (e.g.
        social media, blogging platforms, etc...) to find where those targets have
        active accounts. This can be useful in a social engineering test where you
        have email accounts for a company and want to list where these users have
        used their work email for 3rd party web based services.

    - The ability to quickly create a custom testcase module and use it to enumerate
        for a list of active accounts. Using either a list of know usernames, email
        addresses, or a dictionary of common account names.

    This program is released as is and is not designed to be used to test again sites
    where you do not have permission. Any modules provided are for demonstration purposes
    and may breach end user license agreements if used against a site. Your mileage may
    vary... be responsible!

    External module depenancies:
        colorama (Windows only, optional)

Example Usage:
==============

> List available modules

    ./scythe.py -l

> Check account list against facebook

    ./scythe.py --single facebook.com --accountfile=accountfile.txt

> Check account list against facebook (using threads, w/ summary output)

    ./scythe.py --single facebook.com --accountfile=accountfile.txt --threads 4 --summary

> Check account list against all modules in the social and blogs categories (w/ summary output)

    ./scythe.py --category=social,blogs --accountfile=accountfile.txt --summary

> Check specific accounts against facebook

    ./scythe.py --single facebook.com --account=testuser,testuser2

> Check account list against facebook (output to logfile)

    ./scythe.py --single facebook.com --accountfile=accountfile.txt --output=logfile.txt
    
> Check accounts in the command line against Wordpress.com (3 retries, 60 second retry wait)

    ./scythe.py --single facebook.com --account=testuser,testuser1,testuser2 --retries=3 --retrytime=60
