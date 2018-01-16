Scythe Modules Documentation
============================

This document is designed to provide information for those wishing to create
or edit existing Scythe modules. The Scythe modules are XML based and are 
designed to be flexible in their content. Altough some fields are manditory,
most are optional and can be used based on the requirements of the moduel.


Basic XML Layout
----------------

All modules should contain the basic layout as displayed below.

```
    <!-- tumblr.com - Signup check existing email function -->
        <module>
            <site>
            ....
            </site>
        </module>
```

The intial line is a comment and shold include the website name and a brief
description of the module functionality. The remainder of the XML sets the
basic format of the XML module. More than one <site> sections can be included
where multiple different checks are made against a single website or collection
of websites.

XML Fields
----------

* ```<name>...</name>``` (required)<br>
As suggested, this is the name of the module and will be used (alongside the
filename)when searching for the module using the --single parameter

* ```<url>...</url>``` (required)<br>
As suggested, this field is the URL to be checked against (either GET or POST)
<br><b>Note</b>:
This field should be enclosed in a CDATA tag to avoid problems with the XML
formatting.

* ```<method>...</method>``` (required)<br>
This field must be set to either GET or POST and specifies the type of request

* ```<postParameters>...</postParameters>``` (optional*)<br>
This field sets the parameters to send when using the POST method. It is only
required if POST is specified as the request method.
<br><b>Note</b>:
This field should be enclosed in a CDATA tag to avoid problems with the XML
formatting.

* ```<headers>...</headers>``` (optional)<br>
This comma seperated list of headers is used to set the headers on
the request.
<br><b>Note</b>:
As this field if comma seperated, care should be taken to exclude headers that
contain a comma as part of the key or value.<br>
Many modules specify the Accept-Language: en-gb header in order to ensure the
response received is english (for regex matching purposes)

* ```<requestCookie>[True|False]</requestCookie>``` (optional)<br>
If set to True a cookie will be requested and used on each request. If not
required this should be excluded or set to False as it slows down the application.<br>
```*``` if not set, the application defaults to False

* ```<requestCSRF>...</requestCSRF>``` (optional)<br>
This section/field can either be set to False or contain sub-fields that
are used to specify how and what to extract as a CSRF token.<br>
```*``` if not set, the application defaults to False
<br>
>* ```<csrf_url>...</csrf_url>``` (required*)<br>
Contains the URL to request the CSRF token from (inside CDATA tags)<br>
```*``` This field is only required when <requestCSRF> is set to True<br>
<br>
>* ```<csrf_regex>...</csrf_regex>``` (required*)<br>
Contains the regex used to exctract the CSRF token from the response (Complex
regexs should be enclosed in CDATA tags to prevent XML issues)<br>
```*``` This field is only required when <requestCSRF> is set to True

* ```<successmatch>...</successmatch>``` (required)<br>
This is a regex or string used to match success within the server response
(Complex regexs should be enclosed in CDATA tags to prevent XML issues)

* ```<negativematch>...</negativematch>``` (optional)<br>
This is a regex or string used to match failure within the server response
(Complex regexs should be enclosed in CDATA tags to prevent XML issues)
<br><b>Note</b>:
This is used in debug mode and when success matching is not possible, only
negative matching.

* ```<message>...</message>``` (optional)<br>
This field contains a message when the module is loaded to run that is displayed
to the user. It is used to display information about the module that should be
noted by the user.<br>
<b>example</b>:
    ```<message>Due to the way github works, invlaid email addresses may appear as false positives</message>```

* ```<date>DD/MM/YYYY</date>``` (optional)<br>
Date of the module creation or last edit

* ```<version>...</version>``` (optional)<br>
Module version number

* ```<author>...</author>``` (optional)<br>
The author name, email address or handle

* ```<category>...</category>``` (required)<br>
This field is used to specify the category of the module when loading via the
--category parameter. A number of categories already exist (including: blogs,
social, forums, commerce, ...)<br>
Please keep within those categories where possible.