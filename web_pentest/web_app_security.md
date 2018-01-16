# Web App Penetration Testing

## Unvalidated Redirects and Forwards

Web applications frequently redirect and forward users to other pages and websites, and use untrusted data to determine the destination pages. Without proper validation, attackers can redirect victims to phishing or malware sites, or use forwards to access unauthorized pages.

Here is code from routes/index.js,

```Javascript
// Handle redirect for learning resources link
app.get("/learn", function (req, res, next) {
    return res.redirect(req.query.url);
});
```

An attacker can change the url-query parameter to point to malicious website and share it. Victims are more likely to click on it, as the initial part of the link (before query parameters) points to a trusted site.

### How Do I Prevent It

Safe use of redirects and forwards can be done in a number of ways:

- Simply avoid using redirects and forwards.
- If used, don’t involve user parameters in calculating the destination. This can usually be done.
- If destination parameters can’t be avoided, ensure that the supplied value is valid, and authorized for the user.
- It is recommended that any such destination parameters be a mapping value, rather than the actual URL or portion of the URL, and that server side code translate this mapping to the target URL.

---

## HTTP Parameter Pollution (HPP)

HTTP Parameter Pollution, or HPP, refers to manipulating how a website treats parameters it receives during HTTP requests. The vulnerability occurs when parameters are injected and trusted by the vulnerable website, leading to unexpected behavior. This can happen on the back-end, server-side, where the servers of the site you’re visiting are processing information invisible to you, or on the client-side, where you can see the effect in your client, which is usually your browser.

---

## Cross-Site Request Forgery (CSRF)

A CSRF attack forces a logged-on victim’s browser to send a forged HTTP request, including the victim’s session cookie and any other automatically included authentication information, to a vulnerable web application. This allows the attacker to force the victim’s browser to generate requests that vulnerable application processes are legitimate requests from the victim.

A cross-site request forgery, or CSRF, attack occurs when an attacker can use an HTTP request to access a user’s information from another website, and use that information to act on the user’s behalf. This typically relies on the victim being previously authenticated on the target website where the action is submitted, and occurs without the victim knowing the attack has happened.

---

## Cookies

- When a cookie contains the **secure** attribute, browsers will only send that cookie when visiting HTTPS sites. If you visited http://www.site.com/ with a secure cookie, your browser wouldn’t send your cookies to the site. This is to protect your privacy since HTTPS connections are encrypted and HTTP ones are not.

- The **httponly** attribute tells the browser that the cookie can only be read through HTTP and HTTPS requests. Browsers won’t allow any scripting languages, such as JavaScript, to read its value.

- Lastly, the **expiry date** simply informs the browser of when the site will no longer consider the cookie to be valid, so the browser should destroy it.

---

## HTML Injection

HTML injection is a type of injection issue that occurs when a user is able to control an input point and is able to inject arbitrary HTML code into a vulnerable web page. This vulnerability can have many consequences, like disclosure of a user's session cookies that could be used to impersonate the victim, or, more generally, it can allow the attacker to modify the page content seen by the victims.

### How to Test

This vulnerability occurs when the user input is not correctly sanitized and the output is not encoded. An injection allows the attacker to send a malicious HTML page to a victim. The targeted browser will not be able to distinguish (trust) the legit from the malicious parts and consequently will parse and execute all as legit in the victim context.

There is a wide range of methods and attributes that could be used to render HTML content. If these methods are provided with an untrusted input, then there is an high risk of XSS, specifically an HTML injection one. Malicious HTML code could be injected for example via `innerHTML`, that is used to render user inserted HTML code. If strings are not correctly sanitized the problem could lead to XSS based HTML injection. Another method could be `document.write()`

When trying to exploit this kind of issues, consider that some characters are treated differently by different browsers. For reference see the DOM XSS Wiki.

The innerHTML property sets or returns the inner HTML of an element. An improper usage of this property, that means lack of sanitization from untrusted input and missing output encoding, could allow an attacker to inject malicious HTML code.

Example of Vulnerable Code: The following example shows a snippet of vulnerable code that allows an unvalidated input to be used to create dynamic html in the page context:

```Javascript
var userposition=location.href.indexOf("user=");
var user=location.href.substring(userposition+5);
document.getElementById("Welcome").innerHTML=" Hello, "+user;
```

In the same way, the following example shows a vulnerable code using the document.write() function:

```Javascript
var userposition=location.href.indexOf("user=");
var user=location.href.substring(userposition+5);
document.write("<h1>Hello, " + user +"</h1>");
```

In both examples, an input like the following:

http://vulnerable.site/page.html?user=<img%20src='aaa'%20onerror=alert(1)>

will add to the page the image tag that will execute an arbitrary JavaScript code inserted by the malicious user in the HTML context.

---

## 9. CRLF (Carriage Return Line Feed) Injection

A Carriage Return Line Feed (CRLF) Injection vulnerability occurs when an application does not sanitize user input correctly and allows for the insertion of carriage returns and line feeds, input which for many internet protocols, including HTML, denote line breaks and have special significance.

The effect of a CRLF Injection includes HTTP Request Smuggling and HTTP Response Splitting. HTTP Request Smuggling occurs when an HTTP request is passed through a server which processes it and passes it to another server, like a proxy or firewall. This type of vulnerability can result in:

- Cache poisoning, a situation where an attacker can change entries in an application’s cache and serve malicious pages (e.g., containing JavaScript) instead of a proper page
- Firewall evasion, where a request can be crafted using CRLFs to avoid security checks
- Request Hijacking, a situation where an attacker can steal HttpOnly cookies and HTTP authentication information. This is similar to XSS but requires no interaction between the attacker and client

How to test

- `%0D%0A` are particularly significant characters as they can lead to CRLF Injection issues. When hacking, be on the lookout for parameters that are potentially attacker controlled but being reflected back in a HTTP header.
- If they are, start testing the site for their handling of encoded characters, particularly `%0D%0A`.
- If successful, try to take it a step further and combine the vulnerability with a XSS injection for an impactful proof of concept.
- On the other hand, if the server doesn’t respond to %0D%0A think about how you could double encode these characters, passing in `%250D` or adding 3 byte characters in the event the site is mishandling the extra values just as [@filedescriptor](https://hackerone.com/reports/52042) did.

- Be on the lookout for opportunities where a site is accepting your input and using it as part of its return headers, particularly setting cookies. This is particularly significant when it occurs via a GET request as less interaction from the victim is required.

---

## Cross-Site Scripting

There are two things to note here which will help when finding XSS vulnerabilities:

- The vulnerability in this case wasn’t actually on the file input field itself - it was on the name property of the field. So when you are looking for XSS opportunities, remember to play with all input values available.
- The value here was submitted after being manipulated by a proxy. This is key in situations where there may be Javascript validating values on the client side (your browser) before any values actually get back to the site’s server.

- In fact, any time you see validation happening in real time in your browser, it should be a redflag that you need to test that field! Developers may make the mistake of not validating submitted values for malicious code once the values get to their server because they think the browser Javascript code has already handling validations before the input was received.

When searching for XSS vulnerabilities, here are some things to remember:

- Test Everything Regardless of what site you’re looking at and when, always keep hacking! Don’t ever think that a site is too big or too complex to be vulnerable. Opportunities may be staring you in the face asking for a test like wholesale.shopify.com. The stored Google Tagmanager XSS was a result of finding an alternative way to add tags to a site.
- Vulnerabilities can exist on any form value For example, the vulnerability on Shopify’s giftcard site was made possible by exploiting the name field associated with an image upload, not the actual file field itself.
- Always use an HTML proxy when testing When you try submitting malicious values from the webpage itself, you may run into false positives when the site’s Javascript picks up your illegal values. Don’t waste your time. Submit legitimate values via the browser and then change those values with your proxy to executable Javascript and submit that.
- XSS Vulnerabilities occur at the time of rendering Since XSS occurs when browsers render text, make sure to review all areas of a site where values you enter are being used. It’s possible that the Javascript you add won’t be rendered immediately but could show up on subsequent pages. It’s tough but you want to keep an eye out for times when a site is filtering input vs escaping output. If its the former, look for ways to bypass the input filter as developers may have gotten lazy and aren’t escaping the rendered input.
- Test unexpected values Don’t always provide the expected type of values.
- When the HTML Yahoo Mail exploit was found, an unexpected HTML IMG attribute was provided. Think outside the box and consider what a developer is looking for and then try to provide something that doesn’t match those expectations. This includes finding innovative ways for the potential Javascript to be executed, like bypassing the onmousedown event with Google Images.
- Keep an eye out for blacklists If a site isn’t encoding submitted values (e.g., > becomes %gt;, < becomes %lt;, etc), try to find out why. As in the United example, it might be possible that they are using a blacklist which can be circumvented.
- IFrames are your friend IFrames will execute in their own HTML document but still have access to the HTML document they are being embedded in. This means that if there’s some Javascript acting as a filter on the parent HTML document, embedding an IFrame will provide you with a new HTML document that doesn’t have those protections.

### XSS Attacks types

#### Cross Site Scripting Via URL query parameters

Note any URL query parameters and inject a script into each.

#### Cross Site Scripting Via POST parameters

Use Burp-Suite to note POST parameters and inject a script into each.

#### Cross Site Scripting Via Cookie

Use Cookie Manager or Burp-Suite to create a cross site script and inject a script into each cookie. If the page prints the value of the cookie to the screen, the script will execute.

#### Cross Site Scripting Via HTTP Headers

Any time dynamic output is displayed by the browser, think "Cross-Site Scripting". Work backwards from that output to see if there is a way to influence what is output. This could be as simple as entering "123" in the first field, "456" in the second field, and so on. Repeat this for all input including HTTP Headers, Cookie values, Hidden Fields etc. If those inputs show up anywhere in the output investigate further. Dont look for visible output. That will miss most of the output. Search the entire response stream including all the HTTP Headers. If you find your test strings, send in more useful characters such as "<". Some developers sanitize input which may later be output. Others encode (escape) the input. These are nice tries but can result in "FAIL" because the data could be changed after it is input encoded by someone with access to the database, a database corrupting script, or any attempts to filter/sanitize can be flawed/bypassed.

Any time the application uses the HTTP headers there are multiple possibilities. If the HTTP header is output into the page, think XSS. But with HTTP Headers, also consider HTTP Response Splitting. HTTP Headers are delimited (separated) by line-breaks. Check out the RFC on HTTP to see the specification. When an application included some type of input as output into the HTTP Header, it may be possible to inject a line-break. If this is possible, then an actor could also inject a new HTTP Header of there choosing. These two situations are counterparts. XSS via HTTP Headers may occur when HTTP Request Headers are output into the HTTP Response. HTTP Response Splitting may occur when user/database input is output into HTTP Headers.

---

## JSON Hijacking

JSON injection may occur when user or attacker controlled input is later incorporated without being encoded into the web server response. In other words, the attacker can send input which later is incorporated into the JSON response.

This vulnerability requires that you are exposing a JSON service which…

- returns sensitive data.
- returns a JSON array.
- responds to GET requests.
- the browser making the request has JavaScript enabled (very likely the case)
- the browser making the request supports the `__defineSetter__` method.

### Discovery Methodology

JSON injection starts like any injection; find the possible input parameters including adding custom parameters (parameter addition attack) to see if the application will process them and place those inputs into the JSON returned by the server. (If we cannot get our input into the JSON returned by the server, we cannot inject the JSON.)

---

## Access Control Flows

### Bypass a Path Based Access Control Scheme

```Bash
/../../../../../../../../../etc/shadow
```

## CSRF Prompt By-Pass

```HTML
<img
src="http://localhost:8080/WebGoat/attack?Screen=XXX&menu=YYY&transferFunds=5000"
onerror="document.getElementById('image2').src='http://localhost:8080/WebGoat/attack?Screen=XXX&menu=YYY&transferFunds=CONFIRM'">
<img id="image2" >
```
