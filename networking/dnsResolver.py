import socket
import regex as re
from typing import List
from config import Config
from filtering.filter import Filter
from monitoring.__init__ import clientHandler, dnsMonitor
from dnslib.server import DNSServer, DNSRecord, DNSHandler, RR

# Provides the DNS overrides for the InjectorDNSResolver
class DNSOverrides():
    def __init__(self, dnsList : list=[], fullOverride : bool = False) -> None:
        # Full override reroutes ALL traffic trough the HTTPS Proxy
        self.fullOverride = fullOverride
        if not self.fullOverride:
            self.domains = []
            for dns in dnsList:
                self.domains.append(dns)

    # Check if a queryname matches the override pattern
    def matches(self, qn : str) -> bool:
        if (self.fullOverride):
            return True
        match = False
        for domain in self.domains:
            match = re.match(domain, qn)
            if match:
                return match
        return match

# A very simple DNS resolver which redirects DNS querries to the
# HTTPS Proxy or resolves them via a fallback DNS server (e.g the router)
class InjectorDNSResolver:
    def __init__(self) -> None:
        self.dnsOverrides = DNSOverrides(dnsList=Config.DNS_OVERRIDES, fullOverride=Config.DNS_FULL_OVERRIDE)
        try:
            # The DNS server runs on port 53 by default, this can easily be configured
            # in the config file if needed
            self.server = DNSServer(self,port=Config.DNS_PORT,address="0.0.0.0")
            self.server.start_thread()
        except:
            print("DNS Server failed to launch, probably port blocked?")

    # Check wether the DNS server should override the real IP with the Config.HOST_IP
    def shouldOverrideDNS(self, qn : str) -> bool:
        return self.dnsOverrides.matches(qn)

    def createReply(self, request : DNSRecord, qn : str, clientAddress : str, blocked : bool) -> DNSRecord:
        reply = request.reply()

        # If unknown devices should be routed through
        if Config.REDIRECT_UNKNOWN_DEVICES and not clientHandler.isKnownClient(clientAddress):
            print(clientAddress, " not known -> redirecting all traffic to captive portal")
            return InjectorDNSResolver.overrideDNS("captive.portal.", reply) 

        # Blocked -> Return empty reply
        if blocked:
            return reply
        
        # Override DNS or Resolve against fallback DNS server
        # We do not want to override DNS requests from this machine
        # as we would not be able to resolve the real page ourselves...
        return (InjectorDNSResolver.overrideDNS(qn, reply)
                if (self.shouldOverrideDNS(qn) and not clientAddress == Config.HOST_IP 
                                               and not clientAddress == "127.0.0.1")
                else InjectorDNSResolver.resolveAgainstFallbackDNS(request))
    # The resolve function is called when the DNS server receives a request
    # here we do the response altering
    def resolve(self, request : DNSRecord, handler : DNSHandler) -> DNSRecord:
        qn : str = str(request.q.qname)
        clientAddress : str = handler.client_address[0]
        
        # Check if the DNS request is allowed (or even alter it if wanted)
        request, blocked = Filter.dnsFilter.filter(request, qn)
        # Create reply for request and return it
        reply = self.createReply(request, qn, clientAddress, blocked)
        # Monitor DNS traffic if wanted
        if Config.MONITOR_DNS: 
            dnsMonitor.monitor(request, reply, clientAddress)
        return reply

    # Generate a DNS response which points to the HOST_IP
    def overrideDNS(qn : str, reply : DNSRecord) -> DNSRecord:
        reply.add_answer(*RR.fromZone(qn + " 60 A " + Config.HOST_IP))
        return reply

    # Ask the fallback DNS server to resolve the request for us if
    # we do not want to override it
    def resolveAgainstFallbackDNS(request : DNSRecord) -> DNSRecord:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        try:
            sock.sendto(request.pack(),
                    (Config.FALLBACK_DNS_RESOLVER, Config.FALLBACK_DNS_PORT))
            # Timeout is crucuial as otherwise the sock will not be closed
            sock.settimeout(5.0)
            # Receiving the response from the fallback server
            resp, _ = sock.recvfrom(4096)
        except:
            print("Fallback DNS did not respond...")
        sock.close()
        # Finally, parsing the response from the fallback server to make it usable in our context
        return DNSRecord.parse(resp)
