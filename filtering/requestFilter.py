import flask
import regex as re
from typing import Tuple, List, Dict

class RequestFilterList:
    def __init__(self, lines : List[str]) -> None:
        self.rules = []
        for line in lines:
            self.addRule(line)

    def addRule(self, line : str):
        self.rules.append(line)

class RequestFilter:
    def setFilterList(self, filterList : Dict[str, RequestFilterList]) -> None:
        self.filterList = filterList 

    def filter(self, request : flask.Request, site : str, domain : str) -> Tuple[flask.Request, bool]:
        if domain in self.filterList:
            for reg in self.filterList[domain].rules:
                if re.match(reg, site):
                    return request, True
        return request, False