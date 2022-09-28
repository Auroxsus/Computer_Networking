# Computer_Networking
This project is a collection of 5 products: a web server, UDP pinger, mail client, proxy server, and ICMP pinger. All products are meant to demonstrate aspects of computer networking that I've studied in class, such as unreliable connections (UDP) and HTTP messages.

#Project Specifications
All products were completed using Python.

Web Server
---
This product emulates a web request; a browser connects to our product requesting a HTML page held in that server (a GET request), and the server will either reply with the requested page if it has it (a 200 OK message) or an error message (404 Not Found).

UDP Pinger
---
This product emulates a ping command using UDP (instead of ICMP used by most ping programs), sending 10 pings over a UDP connection, receiving a message back if the server is running otherwise it’ll time out, and calculating the round trip time (RTT) for each successful ping.

Mail Client
---
This product uses TCP to connect with a real mail server (Yahoo, Google, ect.) to send emails following the SMTP protocol to any recipient/mail server, with any mail address, simulating sending an email with a browser or mail app. 

Proxy Server
---
This product simulates a proxy server; a browser sends requests for objects embedded in a HTTP page to our product, which then forwards those requests to the site with those objects. In turn, the site sends their response to the product, and it forwards that response back to the browser. In addition, the product is able to handle multiple requests simultaneously.

ICMP Pinger
---
This product is an upgrade from UDP Pinger. What’s new is that it (1) emulates a ping command using ICMP, (2) in addition to RTT, computes packet loss and a summary consisting of the mean, minimum, and maximum RTTs, and (3) what’s being sent and received are ICMP packets (header and all) instead of a single string. 



# How To Improve:
Web Server
---
The web server can be improved by allowing the client to input any type of file (not just an html file) or a url, where in that case the server will save the page of the url then send the saved page to the browser.

UDP Pinger
---
The UDP pinger in the future can have the added functionalities of letting the user determine the amount of pings to send and the chance of packet loss.

Mail Client
---
The mail client can be improved by allowing the user to use gmail since it can be pretty difficult to configure gmail to use SMTPand can be very picky.

Proxy Server
---
The proxy server can be improved by adding error handling like when a client request an object which is not available. Since the proxy server only supports the HTTP GET method we can add support for POST, by including the request body sent in the POST-request. We can also implement the simple ability of a functional caching web pages.

ICMP Pinger
---
The ICMP pinger can be improved by following the official specification in RFC 1739. Following the official specifications we can offer greater feedback and information regarding errors, control messages, and management queries.  
