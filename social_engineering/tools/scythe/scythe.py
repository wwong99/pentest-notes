#! /usr/bin/env python
# -*- coding: utf-8 -*-

#

"""
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

"""

import os
import re
import signal
import urllib
import urllib2
import string
import textwrap
import sys
import traceback
import time
import Queue
import random
from Cookie import BaseCookie
from threading import Thread, activeCount, Lock, current_thread
from random import Random
from optparse import OptionParser, OptionGroup, SUPPRESS_HELP
from array import *
from xml.dom.minidom import parse

__author__ = 'Chris John Riley'
__license__ = 'BSD (3-Clause)'
__version__ = '0.2.81'
__codename__ = 'Lazy Lizard'
__date__ = '24 May 2013'
__maintainer__ = 'ChrisJohnRiley'
__email__ = 'contact@c22.cc'
__status__ = 'Beta'

modules = []
accounts = []
success = []
color = {}
queue = Queue.Queue()
startTime = time.clock()
sigint = False

def logo():
    # because ASCII-art is the future!

    logo = '''
                                                            ,,
                                                     mm   `7MM
                                                     MM     MM
                        ,pP"Ybd  ,p6"bo `7M'   `MF'mmMMmm   MMpMMMb.  .gP"Ya
                        8I   `" 6M'  OO   VA   ,V    MM     MM    MM ,M'   Yb
                        `YMMMa. 8M         VA ,V     MM     MM    MM 8M""""""
                        L.   I8 YM.    ,    VVV      MM     MM    MM YM.    ,
                        M9mmmP'  YMbmd'     ,V       `Mbmo.JMML  JMML.`Mbmmd'
                                           ,V
                                        OOb"      ::: account harvester :::'''

    # add version, codename and maintainer to logo
    print logo
    print string.rjust('ver ' + __version__ + ' (' + __codename__ + ')', 74)
    print string.rjust(__maintainer__, 73)

def extract_module_data(file, module_dom):
    # extract module information from the provided dom

    for each in module_dom:
        try:
            xmlData = {}

            # try/except blocks to handle badly formed XML modules
            try:
                xmlData['name'] = each.getElementsByTagName('name')[0].firstChild.nodeValue
            except (IndexError, AttributeError):
                xmlData['name'] = 'unspecified'

            # set URL - prepend http:// if not present in string
            if not each.getElementsByTagName('url')[0].firstChild.nodeValue.startswith('http'):
                xmlData['url'] = 'http://' + each.getElementsByTagName('url')[0].firstChild.nodeValue
            else:
                xmlData['url'] = each.getElementsByTagName('url')[0].firstChild.nodeValue

            # set Method
            try:
                xmlData['method'] = each.getElementsByTagName('method')[0].firstChild.nodeValue
            except (IndexError, AttributeError):
                # default to GET if not specified
                xmlData['method'] = 'GET'

            # set POST Parameters if set in the module XML
            try:
                if each.getElementsByTagName('postParameters')[0].firstChild.nodeValue.lower() == 'false':
                    # handle instances where people enter False insterad of leaving this field blank
                    xmlData['postParameters'] = ''
                else:
                    xmlData['postParameters'] = \
                        each.getElementsByTagName('postParameters')[0].firstChild.nodeValue
            except (IndexError, AttributeError):
                xmlData['postParameters'] = ''

            # set headers if set in the module XML
            try:
                if each.getElementsByTagName('headers')[0].firstChild.nodeValue.lower() == 'false':
                    # handle instances where people enter False insterad of leaving this field blank
                    xmlData['headers'] = ''
                else:
                    xmlData['headers'] = \
                        each.getElementsByTagName('headers')[0].firstChild.nodeValue.split(",")
            except (IndexError, AttributeError):
                xmlData['headers'] = ''

            # set request cookie if set in the module XML
            try:
                if each.getElementsByTagName('requestCookie')[0].firstChild.nodeValue.lower() == 'true':
                    xmlData['requestCookie'] = True
                else:
                    xmlData['requestCookie'] = False
            except (IndexError, AttributeError):
                xmlData['requestCookie'] = False

            # set csrf mode if set in the module XML
            # Extract csrf_url and csrf_regex if present
            # if not default to False
            try:
                if each.getElementsByTagName('requestCSRF')[0].firstChild.nodeValue.lower() == 'false':
                    xmlData['requestCSRF'] = False
                    # set csrf_url and csrf_regex to False by default
                    xmlData['csrf_url'] = False
                    xmlData['csrf_regex'] = False
                else:
                    xmlData['requestCSRF'] = True
                    if each.getElementsByTagName('csrf_url')[0].firstChild:
                        xmlData['csrf_url'] = \
                            each.getElementsByTagName('csrf_url')[0].firstChild.nodeValue
                    else:
                        # if no specific csrf_url is set, default to xmlData['url']'
                        xmlData['csrf_url'] = xmlData['url']
                    if each.getElementsByTagName('csrf_regex')[0].firstChild:
                        xmlData['csrf_regex'] = \
                            each.getElementsByTagName('csrf_regex')[0].firstChild.nodeValue
                    else:
                        xmlData['csrf_regex'] = 'unspecified'
            except (IndexError, AttributeError):
                # if requestCSRF not present or noneType
                xmlData['requestCSRF'] = False
                xmlData['csrf_url'] = False
                xmlData['csrf_regex'] = False

            # set success match if specified in the module XML
            try:
                xmlData['successmatch'] = \
                    each.getElementsByTagName('successmatch')[0].firstChild.nodeValue
            except (IndexError, AttributeError):
                xmlData['successmatch'] = ''

            # set negative match if specified in the module XML
            try:
                # handle instances where people enter False insterad of leaving this field blank
                if each.getElementsByTagName('negativematch')[0].firstChild.nodeValue.lower() == 'false':
                    xmlData['negativematch'] = ''
                else:
                    xmlData['negativematch'] = \
                        each.getElementsByTagName('negativematch')[0].firstChild.nodeValue
            except (IndexError, AttributeError):
                xmlData['negativematch'] = ''

            # set error match if specified in the module XML
            try:
                # handle instances where people enter False insterad of leaving this field blank
                if each.getElementsByTagName('errormatch')[0].firstChild.nodeValue.lower() == 'false':
                    xmlData['errormatch'] = ''
                else:
                    xmlData['errormatch'] = \
                        each.getElementsByTagName('errormatch')[0].firstChild.nodeValue
            except (IndexError, AttributeError):
                xmlData['errormatch'] = ''

            # set message if specified in the module XML
            try:
                # handle instances where people enter False insterad of leaving this field blank
                if each.getElementsByTagName('message')[0].firstChild.nodeValue.lower() == 'false':
                    xmlData['message'] = ''
                else:
                    xmlData['message'] = \
                        each.getElementsByTagName('message')[0].firstChild.nodeValue
            except (IndexError, AttributeError):
                xmlData['message'] = ''

            # set module date
            try:
                xmlData['date'] = each.getElementsByTagName('date')[0].firstChild.nodeValue
            except (IndexError, AttributeError):
                xmlData['date'] =  'unspecified'

            # set module version if specified in the module XML
            try:
                xmlData['version'] = each.getElementsByTagName('version')[0].firstChild.nodeValue
            except (IndexError, AttributeError):
                xmlData['version'] = 'unspecified'

            # set module author
            try:
                xmlData['author'] = each.getElementsByTagName('author')[0].firstChild.nodeValue
            except (IndexError, AttributeError):
                xmlData['author'] = 'unlisted'

            # set category
            try:
                xmlData['category'] = each.getElementsByTagName('category')[0].firstChild.nodeValue
            except (IndexError, AttributeError):
                xmlData['category'] = 'unspecified'

            # filter modules based on selected categories
            if xmlData['category'].lower() in (cat.lower() for cat in opts.category) or \
                "all" in (cat.lower() for cat in opts.category) or \
                (opts.single.lower() and opts.single.lower() in xmlData['name'].lower()) or \
                (file.lower() in opts.single.lower()):
                if xmlData['category'].lower() == "example" and \
                    ("example" not in (cat.lower() for cat in opts.category) \
                    and not opts.single):
                    # skip example module when running with all or default settings
                    if opts.verbose:
                        print "\t[" + color['red'] + "!" + color['end'] \
                            + "] Skipping example module : %s" % xmlData['name']
                else:
                    print "\t[" + color['yellow'] + "+" + color['end'] \
                        +"] Extracted module information from %s" \
                        % xmlData['name']
                    modules.append(xmlData)

                # print module message if present
                if xmlData['message']:
                    print textwrap.fill(("\t[" + color['yellow'] + "!" + color['end'] \
                            +"] "+ color['red'] + "Note" + color['end'] +" [%s]:" \
                            % xmlData['name']),
                            initial_indent='', subsequent_indent='\t -> ', width=100)
                    print textwrap.fill(("\t -> %s" % xmlData['message']),
                            initial_indent='', subsequent_indent='\t -> ', width=80)

            else:
                if opts.debug and not opts.category == "single":
                    print "\t[" + color['red'] + "!" + color['end'] \
                        + "] Skipping module %s. Not in category (%s)" \
                        % (xmlData['name'], opts.category)



        except Exception, ex:
            print "\t[" + color['red'] + "!" + color['end'] \
                + "] Failed to extracted module information\n\t\tError: %s" % ex
            if opts.debug:
                print "\n\t[" + color['red'] + "!" + color['end'] + "] ",
                traceback.print_exc()
            continue

def output_modules():
    # print information about the loaded module(s)

    print "\n ------------------------------------------------------------------------------"
    print string.center(color['yellow'] + ">>>>>" + color['end'] + " Module Information " + \
        color['yellow'] + "<<<<<" + color['end'], 100)
    print " ------------------------------------------------------------------------------"
    if opts.verbose and not opts.listmodules:
        for mod in modules:
            print textwrap.fill((" NAME: %s" % mod['name']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print textwrap.fill((" URL: %s" % mod['url']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print textwrap.fill((" METHOD: %s" % mod['method']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print textwrap.fill((" HEADERS: %s" % mod['headers']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print textwrap.fill((" POST PARAMETERS: %s" % mod['postParameters']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print textwrap.fill((" REQUEST COOKIE: %s" % mod['requestCookie']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print textwrap.fill((" REQUEST CSRF TOKEN: %s" % mod['requestCSRF']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print textwrap.fill((" SUCCESS MATCH: %s" % mod['successmatch']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print textwrap.fill((" NEGATIVE MATCH: %s" % mod['negativematch']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print textwrap.fill((" ERROR MATCH: %s" % mod['errormatch']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print textwrap.fill((" MODULE NOTE: %s" % mod['message']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print textwrap.fill((" DATE: %s" % mod['date']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print textwrap.fill((" VERSION: %s" % mod['version']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print textwrap.fill((" AUTHOR: %s" % mod['author']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print textwrap.fill((" CATEGORY: %s" % mod['category']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print " ------------------------------------------------------------------------------"
    else:
        print " ", "| Name |".ljust(35), "| Category |".ljust(26), "| Version |".ljust(8)
        print " ------------------------------------------------------------------------------"
        for mod in modules:
            print "  " + mod['name'].ljust(37) + mod['category'].ljust(30) + mod['version'].ljust(10)
        print " ------------------------------------------------------------------------------\n"
        # exit after providing module list
        sys.exit(0)

def output_accounts():
    # print information about the accounts loaded from accountfile

    print "\n ------------------------------------------------------------------------------"
    print string.center(color['yellow'] + ">>>>>" + color['end'] + " Accounts Loaded " + \
        color['yellow'] + "<<<<<" + color['end'], 100)
    print " ------------------------------------------------------------------------------"
    for a in accounts:
        print textwrap.fill((" Account name: %s" % a),
            initial_indent='', subsequent_indent=' -> ', width=80)
    print " ------------------------------------------------------------------------------\n"

def output_success():
    # print information about success matches

    if opts.summary or (opts.verbose and opts.summary):
        print "\n ------------------------------------------------------------------------------"
        print string.center(color['yellow'] + ">>>>>" + color['end'] + " Successful Matches " + \
        color['yellow'] + "<<<<<" + color['end'], 100)
        print " ------------------------------------------------------------------------------"
        s_success = sorted(success, key=lambda k: k['name']) # group by site name
        # print normal summary table on request (--summary)
        if not opts.verbose and opts.summary:
            print "\n ------------------------------------------------------------------------------"
            print " ", "| Module |".ljust(35), " | Account |".ljust(28)
            print " ------------------------------------------------------------------------------"
            for s in s_success:
                print "  " + s['name'].ljust(37) + s['account'].ljust(30)
            print " ------------------------------------------------------------------------------\n"
        # print verbose summary on request (-v --summary)
        elif opts.verbose and opts.summary:
            for s in s_success:
                print textwrap.fill((" NAME: \t\t\t%s" % s['name']),
                    initial_indent='', subsequent_indent='\t -> ', width=80)
                print textwrap.fill((" ACCOUNT: \t\t%s" % s['account']),
                    initial_indent='', subsequent_indent='\t -> ', width=80)
                print textwrap.fill((" URL: \t\t\t%s" % s['url']),
                    initial_indent='', subsequent_indent='\t -> ', width=80)
                print textwrap.fill((" METHOD: \t\t%s" % s['method']),
                    initial_indent='', subsequent_indent='\t -> ', width=80)
                print textwrap.fill((" POST PARAMETERS: \t%s" % s['postParameters']),
                    initial_indent='', subsequent_indent='\t -> ', width=80)
                print " ------------------------------------------------------------------------------"
    else:
        print " ------------------------------------------------------------------------------\n"

def load_modules():
    # load the modules from moduledir
    # only XML files are permitted

    if not "all" in (cat.lower() for cat in opts.category):
    # using options from command line
        if opts.verbose:
            print " [" + color['yellow'] + "-" + color['end'] \
                + "] using command line supplied category : %s" \
                % ", ".join(opts.category)

    for (path, dirs, files) in os.walk(opts.moduledir):
        for d in dirs:
           if d.startswith("."): # ignore hidden . dirctories
               dirs.remove(d)
        print " [" + color['yellow'] + "-" + color['end'] \
            +"] Starting to load modules from %s" % path
        for file in files:
            if not path.endswith('/'):
                path = path + '/'
            # read in modules
            if file.endswith('.xml') and not file.startswith('.'):
                if opts.verbose:
                    print "\t[ ] Checking module : %s" % file
                try:
                    module_dom = parse(path + file)
                    module_dom = module_dom.getElementsByTagName('site')
                    extract_module_data(file, module_dom)
                except:
                    print "\t[" + color['red'] + "!" + color['end'] \
                        +"] Error parsing %s module, check XML" % file
            elif opts.debug:
                print "\t[" + color['red'] + "!" + color['end'] \
                    + "] Skipping non-XML file : %s" % file

    if opts.verbose or opts.listmodules:
        output_modules()  #debug and module output

def load_accounts():
    # if account is passed in we use that, otherwise
    # load accounts from accountfile
    # one account per line

    if opts.account:
    # load account from command line
        if opts.verbose:
            print " [" + color['yellow'] + "-" + color['end'] \
                + "] using command line supplied user(s) : %s" \
                % ", ".join(opts.account)
        for a in opts.account:
            # add all command line accounts to array for testcases
                if a: # ignore empty fields
                    accounts.append(a)

    else:
    # load accounts from file if it exists
        if not os.path.exists(opts.accountfile):
            print "\n [" + color['red'] + "!" + color['end'] \
                + "] The supplied file  (%s) does not exist!" \
                % opts.accountfile
            sys.exit(0)
        account_file = open(opts.accountfile, 'r')
        account_read = account_file.readlines()
        account_read = [item.rstrip() for item in account_read]
        for a in account_read:
            if not a.startswith("#"): # ignore comment lines in accountfile
                accounts.append(a)

    if opts.verbose:
        output_accounts()  # debug output

def create_testcases():
    # create a list of testcases from accounts and modules
    #
    # replace functions are in place to replace <ACCOUNT>
    #  with the account names presented
    # the script will also replace any instances of <RANDOM>
    #  with a random string (8) to avoid detection

    testcases = []
    tempcase = {}
    for a in accounts:
        for m in modules:
            rand = ''.join( Random().sample(string.letters+string.digits, 8) ) # 8 random chars
            tempcase['url'] = m['url'].replace("<ACCOUNT>", a).replace("<RANDOM>", rand)
            tempcase['account'] = a
            tempcase['name'] = m['name']
            tempcase['method'] = m['method']
            tempcase['postParameters'] = m['postParameters'].replace("<ACCOUNT>", a).replace("<RANDOM>", rand)
            tempcase['headers'] = m['headers']
            tempcase['requestCookie'] = m['requestCookie']
            tempcase['requestCSRF'] = m['requestCSRF']
            tempcase['csrf_url'] = m['csrf_url']
            tempcase['csrf_regex'] = m['csrf_regex']
            tempcase['successmatch'] = m['successmatch']
            tempcase['negativematch'] = m['negativematch']
            tempcase['errormatch'] = m['errormatch']
            testcases.append(tempcase)
            tempcase = {}
    if testcases:
        return testcases
    else:
        print " [" + color['red'] + "!" + color['end'] + \
            "] No testcases created, check your accounts and module settings"
        print
        sys.exit(0)

def request_handler(testcases):
    # handle requests present in testcases

    print "\n ------------------------------------------------------------------------------"
    print string.center(color['yellow'] + ">>>>>" + color['end'] + " Testcases " + \
        color['yellow'] + "<<<<<" + color['end'], 100)
    print " ------------------------------------------------------------------------------"

    print " [" + color['yellow'] + "-" + color['end'] \
            +"] Starting testcases (%d in total)" % len(testcases)
    if opts.wait:
        print " [" + color['yellow'] + "-" + color['end'] \
            +"] Throttling in place (%.2f seconds)\n" % opts.wait
    elif opts.threads:
        print " [" + color['yellow'] + "-" + color['end'] \
            +"] Threading in use (%d threads max)\n" % opts.threads
    else:
        print

    progress = 0 # initiate progress count

    if opts.threads > 1:
        threads = []
        for test in testcases:
            # add testcases to queue
            queue.put(test)

        # create progress update lock
        progress_lock = Lock()

        while not queue.empty() and not sigint:
            # only allow a limited number of threads
            if opts.threads >= activeCount() and not sigint:
                # get next test from queue
                test = queue.get()
                try:
                    # setup thread to perform test
                    t = Thread(target=make_request, args=(test,))
                    t.daemon=True
                    threads.append(t)
                    t.start()
                finally:
                    # iterate progress value for the progress bar
                    progress = len(testcases) - queue.qsize()
                    # call progressbar
                    progress_lock.acquire()
                    try:
                        progressbar(progress, len(testcases))
                    finally:
                        progress_lock.release()
                    # mark task as done
                    queue.task_done()

        # wait for queue and threads to end before continuing
        while activeCount() > 1:
            # keep main program active to catch keyboard interrupts
            time.sleep(0.1)

        for thread in threads:
            thread.join()

        # no more active threads. resolve queue
        queue.join()

    else:
        for test in testcases:
            # make request without using threading
            make_request(test)
            # iterate progress value for the progress bar
            progress = progress +1
            # call progressbar
            progressbar(progress, len(testcases))

            if opts.wait: # wait X seconds as per wait setting
                time.sleep(opts.wait)

    return

def progressbar(progress, total):
    # progressbar

    if total > 50: # only show progress on tests of > 50
        if not progress == 0:
            # set percentage
            progress_percentage = int(100 / (float(total) / float(progress)))
            # display progress at set points
            total = float(total)
            # calculate progress for 25, 50, 75, and 99%
            vals = [int(total/100*25), int(total/100*50), int(total/100*75), int(total-1)]
            if progress in vals:
                print " [" + color['yellow'] + "-" + color['end'] +"] [%s] %s%% complete\n" \
                    % ((color['yellow'] + ("#"*(progress_percentage / 10)) + \
                    color['end']).ljust(10, "."),progress_percentage),

def make_request(test, retry=0, wait_time=False):
    # make request and add output to array

    # set threadname
    if not current_thread().name == 'MainThread':
        threadname = "[" + current_thread().name +"] >"
    else:
        # return blank string when not using threading
        threadname = '>'

    # GET method worker
    if test['method'] == 'GET':
        test, resp, r_info, req = get_request(test)

        # success match
        if resp and test['successmatch']:
            matched = success_check(resp, test['successmatch'])
            if matched:
                print " [" + color['green'] + "X" + color['end'] + "] Account %s exists on %s" \
                    % (test['account'], test['name'])
                success.append(test)
                if opts.debug:
                    print # spacing forverbose output
                if opts.outputfile:
                    # log to outputfile
                    opts.outputfile.write("Account " + test['account'] + " exists on " \
                        + test['name'] +"\n")

        # error match
        if resp and test['errormatch']:
            error = error_check(resp, test['errormatch'])
            if error and retry >= opts.retries:
                print " [" + color['red'] + "!" + color['end'] + \
                    "] %s Retries exceeded when testing account %s on %s" \
                    % (threadname, test['account'], test['name'])

            elif error:
                print " [" + color['yellow'] + "!" + color['end'] + \
                    "] %s Error detected when testing account %s on %s" \
                    % (threadname, test['account'], test['name'])
                # wait X seconds and retry
                if wait_time:
                    # double existing wait_time
                    wait_time = wait_time * 2
                else:
                    # set starting point for wait_time
                    wait_time = opts.retrytime
                if opts.verbose:
                    print " [ ] %s Waiting %d seconds before retry" \
                        % (threadname, wait_time)
                time.sleep(wait_time)
                # increment retry counter
                retry = retry + 1
                if opts.verbose:
                    print " [ ] %s Attempting retry (%d of %d)" \
                        % (threadname, retry, opts.retries)
                make_request(test, retry, wait_time)
                return

        # negative match
        if resp and test['negativematch']:
            matched = negative_check(resp, test['negativematch'])
            if matched and opts.verbose:
                print " [" + color['red'] + "X" + color['end'] + "] Negative matched %s on %s" \
                    % (test['account'], test['name'])

        # advance debug output
        if resp and opts.debugoutput:
            debug_save_response(test, resp, r_info, req)

        return

    # POST method worker
    elif test['method'] == 'POST':
        test, resp, r_info, req = post_request(test)

        # success match
        if resp and test['successmatch']:
            matched = success_check(resp, test['successmatch'])
            if matched:
                print " [" + color['green'] + "X" + color['end'] + "] Account %s exists on %s" \
                    % (test['account'], test['name'])
                success.append(test)
                if opts.debug:
                    print # spacing forverbose output
                if opts.outputfile:
                    # log to outputfile
                    opts.outputfile.write("Account " + test['account'] + " exists on " \
                        + test['name'] +"\n")

        # error match
        if resp and test['errormatch']:
            error = error_check(resp, test['errormatch'])
            if error and retry >= opts.retries:
                print " [" + color['red'] + "!" + color['end'] + \
                    "] %s Retries exceeded when testing account %s on %s" \
                    % (threadname, test['account'], test['name'])
            elif error:
                print " [" + color['yellow'] + "!" + color['end'] + \
                    "] %s Error detected when testing account %s on %s" \
                    % (threadname, test['account'], test['name'])
                # wait X seconds and retry
                if wait_time:
                    # double existing wait_time
                    wait_time = wait_time * 2
                else:
                    # set starting point for wait_time
                    wait_time = opts.retrytime
                if opts.verbose:
                    print " [ ] %s Waiting %d seconds before retry" \
                        % (threadname, wait_time)
                time.sleep(wait_time)
                # increment retry counter
                retry = retry + 1
                if opts.verbose:
                    print " [ ] %s Attempting retry (%d of %d)" \
                        % (threadname, retry, opts.retries)
                make_request(test, retry, wait_time)

        # negative match
        if resp and test['negativematch']:
            matched = negative_check(resp, test['negativematch'])
            if matched and opts.verbose:
                print " [" + color['red'] + "X" + color['end'] + "] Negative matched %s on %s" \
                    % (test['account'], test['name'])

        if resp and opts.debugoutput:
            debug_save_response(test, resp, r_info, req)

        return

    else:
        print " [" + color['red'] + "!" + color['end'] + "] Unknown Method %s : %s" \
            % test['method'], test['url']
        return

def get_request(test):
    # perform GET request

    urllib.urlcleanup() # clear cache

    try:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        req_headers = { 'User-Agent' : user_agent }
        for each in test['headers']:
            key, val = each.split(":", 1)
            key = key.lstrip()
            val = val.lstrip()
            req_headers[key] = val
        if test['requestCookie'] or test['requestCSRF']:
            # request cookie and csrf token if set in module XML
            cookie_val, csrf_val = request_value(test)
            if cookie_val:
                req_headers['cookie'] = cookie_val
            if csrf_val:
                # replace <CSRFTOKEN> with the collected token
                test['url'] = test['url'].replace("<CSRFTOKEN>", csrf_val)
                test['postParameters'] = test['postParameters'].replace("<CSRFTOKEN>", csrf_val)
                test['headers'] = [h.replace('<CSRFTOKEN>', csrf_val) for h in test['headers']]

        if opts.debug:
            # print debug output
            print textwrap.fill((" [ ] URL (GET): %s" % test['url']),
                initial_indent='', subsequent_indent=' -> ', width=80)
            print

        # assign NullHTTPErrorProcessor as default opener
        opener = urllib2.build_opener(NullHTTPErrorProcessor())
        urllib2.install_opener(opener)

        req = urllib2.Request(test['url'], headers=req_headers)
        f = urllib2.urlopen(req)
        r_body = f.read()
        r_info = f.info()
        f.close()

        # handle instances where the response body is 0 bytes in length
        if not r_body:
            print " [" + color['red'] + "!" + color['end'] + "] Zero byte response received from %s" \
                % test['name']
            r_body = "<Scythe Message: Empty response from server>"

        # returned updated test and response data
        return test, r_body, r_info, req

    except Exception:
        print textwrap.fill((" [" + color['red'] + "!" + color['end'] + "] Error contacting %s" \
            % test['url']), initial_indent='', subsequent_indent='\t', width=80)
        if opts.debug:
            for ex in traceback.format_exc().splitlines():
                print textwrap.fill((" %s" \
                    % str(ex)), initial_indent='', subsequent_indent='\t', width=80)
            print
        return test, False, False, req

def post_request(test):
    # perform POST request

    urllib.urlcleanup() # clear cache

    try:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        req_headers = { 'User-Agent' : user_agent }

        if test['requestCookie'] or test['requestCSRF']:
            # request cookie and csrf token if set in module XML
            cookie_val, csrf_val = request_value(test)
            if cookie_val:
                req_headers['cookie'] = cookie_val
            if csrf_val:
                # replace <CSRFTOKEN> with the collected token
                test['url'] = test['url'].replace("<CSRFTOKEN>", csrf_val)
                test['postParameters'] = test['postParameters'].replace("<CSRFTOKEN>", csrf_val)
                test['headers'] = [h.replace('<CSRFTOKEN>', csrf_val) for h in test['headers']]

        if test['headers']:
            for each in test['headers']:
                key, val = each.split(":", 1)
                key = key.lstrip()
                val = val.lstrip()
                req_headers[key] = val

        if opts.debug:
            # print debug output
            print textwrap.fill((" [ ] URL (POST): %s" % test['url']),
                initial_indent='', subsequent_indent='  -> ', width=80)
            print textwrap.fill((" [ ] POST PARAMETERS: %s" % test['postParameters']),
                initial_indent='', subsequent_indent='  -> ', width=80)
            print

        # assign NullHTTPErrorProcessor as default opener
        opener = urllib2.build_opener(NullHTTPErrorProcessor())
        urllib2.install_opener(opener)

        req = urllib2.Request(test['url'], test['postParameters'], req_headers)
        f = urllib2.urlopen(req)
        r_body = f.read()
        r_info = f.info()
        f.close()

        # handle instances where the response body is 0 bytes in length
        if not r_body:
            print " [" + color['red'] + "!" + color['end'] + "] Zero byte response received from %s" \
                % test['name']
            r_body = "<Scythe Message: Empty response from server>"

        # returned updated test and response data
        return test, r_body, r_info, req

    except Exception:
        print textwrap.fill((" [" + color['red'] + "!" + color['end'] + "] Error contacting %s" \
            % test['url']), initial_indent='', subsequent_indent='\t', width=80)
        if opts.debug:
            for ex in traceback.format_exc().splitlines():
                print textwrap.fill((" %s" \
                    % str(ex)), initial_indent='', subsequent_indent='\t', width=80)
            print
        return test, False, False, req

def request_value(test):
    # request a cookie or CSRF token from the target site for use during the logon attempt

    urllib.urlcleanup() # clear cache

    # assign NullHTTPErrorProcessor as default opener
    opener = urllib2.build_opener(NullHTTPErrorProcessor())
    urllib2.install_opener(opener)

    # capture cookie first for use with the CSRF token request

    # capture Set-Cookie
    if test['requestCookie']:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        req_headers = { 'User-Agent' : user_agent }
        if test['csrf_url']:
            # if csrf_url is set, use the same page to collect cookies
            url = test['csrf_url']
        else:
            url = test['url'].split("?", 1)[0] # strip parameters from url where present
        req_val = urllib2.Request(url, headers=req_headers)
        response = urllib2.urlopen(req_val)
        resp_body = response.read()
        if response.info().getheader('Set-Cookie'):
            set_cookie = response.info().getheader('Set-Cookie') # grab Set-cookie
            # work Set-cookie into valid cookies to set
            bcookie = BaseCookie(set_cookie)
            # strip off unneeded attributes (e.g. expires, path, HTTPOnly etc...
            cookie_val = bcookie.output(attrs=[], header="").lstrip()
        else:
            cookie_val = False
            print " [" + color['red'] + "!" + color['end'] \
                + "] Set-Cookie Error: No valid Set-Cookie response received"
    else:
        cookie_val = False

    # capture CSRF token (using regex from module XML)
    if test['requestCSRF']:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        req_headers = { 'User-Agent' : user_agent }
        if cookie_val:
            # if a cookie value exists, use the existing response
            if opts.debug:
                print " [" + color['yellow'] + "-" + color['end'] \
                + "] Using existing response to gather CSRF token"
        else:
            # get new response to work with
            url = test['csrf_url']
            req_val = urllib2.Request(url, headers=req_headers)
            response = urllib2.urlopen(req_val)
        try:
            csrf_regex = re.compile(test['csrf_regex'])
            match = re.search(csrf_regex, resp_body)
            if match:
                csrf_val = match.group(1)
            else:
                csrf_val = False
                print " [" + color['red'] + "!" + color['end'] \
                    + "] Invalid CSRF regex. Please check parameters"
        except:
            print " [" + color['red'] + "!" + color['end'] \
                + "] Invalid CSRF regex. Please check parameters"
            if opts.debug:
                    print "\n\t[" + color['red'] + "!" + color['end'] + "] ",
                    traceback.print_exc()
    else:
        csrf_val = False

    return cookie_val, csrf_val

def error_check(data, errormatch):
    # checks response data against errormatch regex

    try:
        regex = re.compile(errormatch)
        if regex.search(data):
            return True
        else:
            return False
    except:
        print " [" + color['red'] + "!" + color['end'] \
            + "] Invalid in error check. Please check parameter"
        if opts.debug:
            print "\n\t[" + color['red'] + "!" + color['end'] + "] ",
            traceback.print_exc()

def success_check(data, successmatch):
    # checks response data against successmatch regex

    try:
        regex = re.compile(successmatch)
        if regex.search(data):
            return True
        else:
            return False
    except:
        print " [" + color['red'] + "!" + color['end'] \
            + "] Invalid in success check. Please check parameter"
        if opts.debug:
            print "\n\t[" + color['red'] + "!" + color['end'] + "] ",
            traceback.print_exc()

def negative_check(data, negativematch):
    # checks response data against negativematch regex

    try:
        regex = re.compile(negativematch)
        if regex.search(data):
            return True
        else:
            return False
    except:
        print " [" + color['red'] + "!" + color['end'] \
            + "] Invalid in negative check. Please check parameter"
        if opts.debug:
            print "\n\t[" + color['red'] + "!" + color['end'] + "] ",
            traceback.print_exc()

def debug_save_response(test, resp, r_info, req):
    # save advanced deug responses to ./debug/

    # get time to attach to filename
    timenow = int(time.time())
    # set testname, remove spaces
    testname = re.sub(r'[^\w]', '_', test['name']) + "_"

    # check debug directory exists, if not create it
    if not os.path.exists('./debug/'):
        os.makedirs('./debug/')

    # filename for html and headers, strip unusable chars from filenames
    htmlfile = testname + str(timenow)
    htmlfile = './debug/' + re.sub(r'[^\w]', '_', htmlfile) + '.html' # strip unsuitable chars
    hdrfile = testname + str(timenow)
    hdrfile = './debug/' + re.sub(r'[^\w]', '_', hdrfile) + '.headers' # strip unsuitable chars

    # format headers
    header_output = []
    header_output.append('---------------------\nrequest headers\n---------------------\n')
    for key in req.headers:
        header_output.append(key + ': ' + req.headers[key])

    header_output.append('\n---------------------\nresponse headers\n---------------------\n')
    for each in r_info.headers:
        header_output.append(each.rstrip())
    header_output.append('\n')

    # check if file exists, if so add random number to filename
    if os.path.isfile(htmlfile):
        rand_addition = str(random.randint(0000, 9999)).zfill(4)
        htmlfile = htmlfile[:-5] + '_' + rand_addition + '.html'
        hdrfile = hdrfile[:-8] + '_' + rand_addition + '.headers'

    # open file for writing
    f_html = open(htmlfile, 'w')
    f_headers = open(hdrfile, 'w')

    # write response and close
    f_html.write(resp)
    f_html.close()

    # write headers and close
    f_headers.write("\n".join(header_output))
    f_headers.close()

    print " [" + color['yellow'] + ">" + color['end'] + "] Saved debug output to %s[.html|.header]" % htmlfile[:-5]

def signal_handler(signal, frame):
    # handle CTRL + C events

    # globally signal threads to end
    global sigint
    sigint = True # turn on SIGINT

    print
    if not len(success) == 0:
        if opts.summary or (opts.verbose and opts.summary):
            print " [" + color['red'] + "!" + color['end'] \
                + "] Outputting successful findings and closing\n"
        output_success()
    print " [" + color['yellow'] + "-" + color['end'] \
            +"] tests stopped after %.2f seconds" % (time.clock() - startTime)
    print "\n [" + color['red'] + "!" + color['end'] + "] Ctrl+C detected... exiting\n"
    if opts.outputfile and not isinstance(opts.outputfile, str):
        # if opts.outputfile is an open file, close it to save output
        opts.outputfile.close()
    os._exit(1)

def query_user(question, default='no'):
    # query user for Y/N response

    valid = {"yes":True, "y":True, "no":False, "n":False}
    if default.lower() == 'yes':
        prompt = " [ " + color['yellow'] + "Y" + color['end'] + "/n ] :"
    else:
        prompt = " [ y/" + color['yellow'] + "N" + color['end'] + " ] :"

    while True:
        print question + prompt,
        try:
            choice = raw_input().lower()
        except:
            print "\n\n [" + color['red'] + "!" + color['end'] \
                + "] Ctrl+C detected... exiting\n"
            sys.exit(0)
        if choice == '':
            if default.lower() == 'yes':
                return valid["yes"]
            else:
                return valid["no"]
        elif choice in valid:
            return valid[choice]
        else:
            print "\t[" + color['red'] + "!" + color['end'] \
                + "] Please respond with 'yes' or 'no'\n"

def setup():
    # setup command line options

    global opts
    parser = OptionParser(version="%prog version ::: " + __version__, epilog="\n")

    # account options grouping
    group = OptionGroup(parser, "Account Options ")
    group.add_option(
        "-a", "--accountfile",
        dest="accountfile",
        default="./accountfile.txt",
        help="Location of the accounts FILE (1 per line)",
        metavar="FILE"
        )
    group.add_option(
        "-u", "--account",
        dest="account",
        default=[],
        action="append",
        help="Account(s) to check (comma seperated, no spaces)",
        metavar="STRING"
        )
    parser.add_option_group(group)

    # module options grouping
    group = OptionGroup(parser, "Module Options ")
    group.add_option(
        "-l", "--list",
        action="store_true",
        dest="listmodules",
        default=False,
        help="List module names and categories",
        )
    group.add_option(
        "-m", "--moduledir",
        dest="moduledir",
        default="./modules/",
        help="Location of the modules directory",
        metavar="DIR"
        )
    group.add_option(
        "-s", "--single",
        dest="single",
        default="",
        help="Restrict to specific module name (XML NAME or filename)",
        metavar="MODULE"
        )
    group.add_option(
        "-c", "--category",
        dest="category",
        default=[],
        action="append",
        help="Restrict modules based on category (comma seperated, no spaces)"
        )
    parser.add_option_group(group)

    # timing options grouping
    group = OptionGroup(parser, "Timing Options ")
    group.add_option(
        "-t", "--threads",
        dest="threads",
        default=0,
        help="Enable threading. Specify max # of threads",
        metavar="INT",
        type="int"
        )
    group.add_option(
        "-w", "--wait",
        dest="wait",
        default=False,
        help="Throttle tests (e.g. -w 0.5 for 0.5 second delay)",
        type="float",
        metavar="SECS"
        )
    group.add_option(
        "--retrytime",
        dest="retrytime",
        default="30",
        help="Wait and retry on errormatch (seconds)",
        type="int",
        metavar="SECS"
        )
    group.add_option(
        "--retries",
        dest="retries",
        default="1",
        help="Number of retries, doubling wait time each retry",
        type="int"
        )
    parser.add_option_group(group)

    # output options grouping
    group = OptionGroup(parser, "Output Options ")
    group.add_option(
        "--summary",
        action="store_true",
        dest="summary",
        default=False,
        help="Show detailed summary before closing",
        )
    group.add_option(
        "-o", "--output",
        dest="outputfile",
        default=False,
        help="Output results to a file as well as screen",
        metavar="FILE"
        )
    parser.add_option_group(group)

    # debug options grouping
    group = OptionGroup(parser, "Debug Options")
    group.add_option(
        "-v", "--verbose",
        action="count",
        dest="verbose",
        help="Print verbose messages to stdout (-vv for very verbose)"
        )
    group.add_option(
        "-d", "--debug",
        action="store_true",
        dest="debugoutput",
        default=False,
        help="Store response and headers in ./debug/"
        )
    group.add_option(
        "-?",
        action="store_true",
        dest="question",
        default=False,
        help=SUPPRESS_HELP
        ) # hidden -? handling
    parser.add_option_group(group)
    (opts, args) = parser.parse_args()

    # the following section reworks options as required

    # set retries to 1 if retrytime  set and not set already
    if not opts.retrytime == 30 and \
        opts.retries == 0:
        # user set retrytime but forgot to set retries to at least 1
        opts.retries = 1

    # split multiple account names into flat list
    if opts.account:
        acc_split = []
        for a in opts.account:
             acc_split.append(a.split(','))
        opts.account = sum(acc_split, [])
        # remove blanks and invalid entries from accounts
        opts.account = filter(None, opts.account)

    # split multiple categories into flat list
    if opts.category:
        cat_split = []
        for c in opts.category:
             cat_split.append(c.split(','))
        opts.category = sum(cat_split, [])
    else:
        # default to all categories
        opts.category = ['all']

    # handle help output
    if opts.question: # print help on -? also
        parser.print_help()
        sys.exit(0)

    # set verbosity level (-v verbose, -v -v verbose and debug)
    if not opts.verbose:
        opts.verbose = False
        opts.debug = False
    elif opts.verbose == 1:
        opts.verbose = True
        opts.debug = False
    elif opts.verbose == 2:
        opts.verbose = True
        opts.debug = True
    elif opts.verbose == 3:
        opts.verbose = True
        opts.debug = True
        # enabled saving of header and response data to ./debug/
        opts.debugoutput = True
    else:
        opts.verbose = True
        opts.debug = True

    # set ansi colors for supported platforms (colorama support for Windows)
    if sys.platform.startswith("win"):
        try:
            import colorama
            colorama.init()
            color['red'] = colorama.Fore.RED + colorama.Style.BRIGHT
            color['green'] = colorama.Fore.GREEN + colorama.Style.BRIGHT
            color['yellow'] = colorama.Fore.YELLOW + colorama.Style.BRIGHT
            color['end'] = colorama.Fore.RESET + colorama.Style.RESET_ALL
        except:
            # disable colors on systems without colorama installed
            print "\n\t[!] Colorama Python module not found, color support disabled"
            color['red'] = ""
            color['green'] = ""
            color['yellow'] = ""
            color['end'] = ""
    else:
        # set colors for non-Windows systems
        color['red'] = "\033[1;31m"
        color['green'] = "\033[1;32m"
        color['yellow'] = "\033[1;33m"
        color['end'] = "\033[0m"

    # error on wait AND threads
    if opts.wait and opts.threads > 0:
        parser.print_help()
        parser.exit(0, "\n\t[" + color['red'] + "!" + color['end'] \
                +"] Please don't set throttling (wait) AND threading!\n")

    # clear category if single module specified
    if opts.single:
        opts.category = "single"

    # clear accountfile if account specified at command line
    if opts.account:
        opts.accountfile = "none"

    # display selected options for the user
    display_options()

    # default user_input for cases where none is required
    user_input = "none"

    # attempt to handle situations where no module or account file is specified
    # skip section if module output is selected
    if (opts.moduledir == './modules/' and opts.accountfile == './accountfile.txt') \
        and not opts.listmodules and not opts.account and \
        "all" in (cat.lower() for cat in opts.category):
        # accountdir and moduledir are default single/specific account mode not enabled
        print "\t[ ] No command-line options specified"
        # prompt user as this could be dangerous
        user_input = query_user("\t[" + color['yellow'] + "?" + color['end'] \
            +"] Test accounts in accountfile.txt against ALL modules? (dangerous)", 'no')

    # vary prompts cased on selected options
    # case: account(s) specified but modules not set
    elif opts.account and opts.moduledir == './modules/' and \
        not opts.single and "all" in (cat.lower() for cat in opts.category):
        user_input = query_user("\t[" + color['yellow'] + "?" + color['end'] \
            +"] Test provided account(s) against ALL modules?", 'yes')
    # case: module set but accountfile left at default
    elif opts.single and opts.accountfile == './accountfile.txt':
        user_input = query_user("\t[" + color['yellow'] + "?" + color['end'] \
            +"] Test usernames in accountfile.txt against the selected module?", 'yes')
    # case: category set but accountfile left at default
    elif opts.category and opts.accountfile == './accountfile.txt' \
        and not opts.listmodules:
        user_input = query_user("\t[" + color['yellow'] + "?" + color['end'] \
            +"] Test accounts in accountfile.txt against selected category?", 'yes')

    # handle user_input
    if user_input:
        # continue using defaults
        if not user_input == "none":
            print "\t[ ] Continuing...."
    else:
        print
        parser.print_help()
        parser.exit(0, "\t[" + color['red'] + "!" + color['end'] \
            +"] Please specify arguments\n")

    # check if outputfile exists already and prompt to overwrite
    if opts.outputfile:
        if os.path.exists(opts.outputfile):
            # query user to overwrite existing outputfile
            user_input = query_user("\t[" + color['yellow'] + "?" + color['end'] \
                +"] Overwrite existing outputfile?", 'no')
            if user_input:
                print "\t[ ] Overwriting output file : %s\n" % opts.outputfile
            else:
                sys.exit("\n\t[" + color['red'] + "!" + color['end'] \
                +"] Please specify new output file\n")
        # open output file
        try:
            opts.outputfile = open(opts.outputfile, "w")
        except:
            print " [" + color['red'] + "!" + color['end'] \
                + "] Unable to open output file for writing"
            if opts.debug:
                print "\n\t[" + color['red'] + "!" + color['end'] + "] ",
                traceback.print_exc()

def display_options():
    # print out the options being used

    print "\n ------------------------------------------------------------------------------"
    # display accountfile if accounts not specified at commandline
    if not opts.account:
        print "\t[" + color['yellow'] + "-" + color['end'] +"] Account File :::".ljust(30), \
            str(opts.accountfile).ljust(40)
    else:
        print "\t[" + color['yellow'] + "-" + color['end'] +"] Account(s) :::".ljust(30), \
            ", ".join(opts.account).ljust(40)

    # print module directory
    print "\t[" + color['yellow'] + "-" + color['end'] +"] Module Directory :::".ljust(30), \
        str(opts.moduledir).ljust(40)

    # print categories if not single
    if not opts.single:
        print "\t[" + color['yellow'] + "-" + color['end'] +"] Categories :::".ljust(30), \
            ", ".join(opts.category).ljust(40)
    else:
        print "\t[" + color['yellow'] + "-" + color['end'] +"] Single Module :::".ljust(30), \
            str(opts.single).ljust(40)

    # display debug level
    if opts.debugoutput:
        print "\t[" + color['yellow'] + "-" + color['end'] +"] Verbose :::".ljust(30), \
            "Debug output to ./debug/".ljust(40)
    elif opts.debug:
        print "\t[" + color['yellow'] + "-" + color['end'] +"] Verbose :::".ljust(30), \
            "Very Verbose".ljust(40)
    else:
        print "\t[" + color['yellow'] + "-" + color['end'] +"] Verbose :::".ljust(30), \
            "Verbose".ljust(40)

    # create outputfile and display filename
    if opts.outputfile:
        # get filename based on current path
        file = os.path.realpath(opts.outputfile).replace(os.getcwd(), "")
        if file.startswith("\\") or file.startswith("/"):
            # strip leading \ from file display
            file = file[1:]
        print "\t[" + color['yellow'] + "-" + color['end'] +"] Output :::".ljust(30), \
            str(file).ljust(40)

    # display wait, threads and retries if specified
    if opts.wait:
        print "\t[" + color['yellow'] + "-" + color['end'] +"] Throttling :::".ljust(30), \
            str(opts.wait) + " seconds".ljust(40)
    if opts.threads:
        print "\t[" + color['yellow'] + "-" + color['end'] +"] Threads :::".ljust(30), \
            str(opts.threads) + " threads".ljust(40)
    if opts.retries:
        print "\t[" + color['yellow'] + "-" + color['end'] +"] Retries (delay) :::".ljust(30), \
            str(opts.retries) + " (" + str(opts.retrytime) + " secs)".ljust(40)
    print " ------------------------------------------------------------------------------\n"

class NullHTTPErrorProcessor(urllib2.HTTPErrorProcessor):
    # return contents without throwing errors (not everything in life is a 200 OK)
    def http_response(self, request, response):
        return response
    def https_response(self, request, response):
        return response


def main():
    logo()
    setup()
    load_modules()
    load_accounts()
    testcases = create_testcases()
    request_handler(testcases)

    # print success matches at the end
    print "\n [" + color['yellow'] + "-" + color['end'] \
        +"] tests completed in %.2f seconds" \
        % (time.clock() - startTime)
    if len(success) > 0:
        print " [" + color['yellow'] + "+" + color['end'] \
            +"] %d matches found" \
            % len(success)
        output_success()
    else:
        sys.exit("\n\t[" + color['red'] + "!" + color['end'] \
            + "] No matches found. Exiting!")

signal.signal(signal.SIGINT, signal_handler)
main()
