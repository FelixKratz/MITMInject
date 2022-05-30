from dnslib.dns import DNSRecord
from typing import Tuple, List, Dict

class DNSFilter:
    def setFilterList(self, filterList : Dict[str,List[str]]) -> None:
        filters = []
        for key in filterList:
            filters.append(filterList[key])
        self.filterList = filters

    def filter(self, request : DNSRecord, qn : str) -> Tuple[DNSRecord, bool]:
        if (qn in self.filterList):
            return request, True
        return request, False