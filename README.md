# InjectionServer
This software can alter the appearance or functionality of arbitrary websites on a network wide level, allowing for website extensions or ad filtering even on devices
that have no or limited built in browser plugin capability.

The way this works is the following, while calling the device running this software the "router" (this software does not need to run on a router specifically, 
it can also run on a raspberry pi for example):
* All DNS requests targeted at router are inspected and when a website match is found in the list of websites to alter the
DNS request gets answered with a forged IP answer pointing to the router.
* The client gets the DNS resolve and points all further requests at the router
* The router now needs to authenticate to the client (if using https) with a valid certificate for the requested domain.
This is achieved by creating a own certificate authority which signs the website certificates on the fly and needs to be trusted
by the client (todo: explain how the trust from client works).
* After the successful handshake between router and client the website content is requested by the client.
The router takes this request, alters it in the wanted ways (e.g. dropping ad-content requests, or deleting personal information from the request) and
forwards them to the "real" website, which then sends a content response to the router. Because the router forwarded the original request as a "man-in-the-middle"
it can read the delivered content.
* The original content response from the website is filtered and altered by the router in the wanted ways
* Finally, the router deliveres the modified website to the client device, where no more filtering and blocking has to be performed

Essentially, this takes the webfiltering achieved with browser plugins like Ublock or adblockPlus off of the client device and offloads it to
a capable machine, which can perform the filtering for the whole network.
In addition to DNS blockers like Pi-Hole it is possible to fully alter the website and "inject" additional code into the site (e.g. a JSON parse proxy which is needed to filter
certain ads or trackers).
This allows powerful webfiltering and plugins on devices that do not support these plugins out-of-the-box (e.g. safari on iOS etc.).
