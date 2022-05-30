from dnslib.server import DNSRecord
from monitoring.monitor import Monitor, HistoryElement

class DNSHistoryElement(HistoryElement):
    def __init__(self, request : DNSRecord, reply : DNSRecord, clientAddress : str):
        super().__init__()
        self.request = request
        self.reply = reply
        self.clientAddress = clientAddress
        self.responseIP = str(self.reply)
        self.requestedDomainName = str(self.request.q.qname)

    # String representation of the DNSHistoryElement which is displayed
    def __str__(self) -> str:
        return self.timeStamp + " -- " + self.clientAddress + ": Issued DNS request " + self.requestedDomainName + " ---> " + self.responseIP
    
    # String representation of the DNSHistoryElement which is logged
    def __repr__(self) -> str:
        return ""

class DNSMonitor(Monitor):
    def __init__(self):
        super().__init__()

    def monitor(self, request : DNSRecord, reply : DNSRecord, clientAddress : str) -> None:
        self.addToHistory(DNSHistoryElement(request, reply, clientAddress))
