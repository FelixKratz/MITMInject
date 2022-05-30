import flask
import regex as re
from config import Config
from typing import Tuple, List, Dict

class PruneFilterList:
    def __init__(self, lines : List[str]) -> None:
        self.rules = []
        for line in lines:
            self.addRule(line)

    def addRule(self, line : str):
        self.rules.append(line)

class PruneFilter:
    def setFilterList(self, filterList : Dict[str, PruneFilterList]) -> None:
        self.filterList = filterList
        self.injections = {}

    def generateInjection(self, domain : str) -> bytes:
        if (domain in self.injections):
            return self.injections[domain]
        injection = b""
        if domain in self.filterList:
            for rule in self.filterList[domain].rules:
                injection += b"System.pushJSONParseProxy(\"" + rule.encode("UTF-8") + b"\");\n"
        self.injections[domain] = injection
        return injection
