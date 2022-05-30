import flask
import regex as re
from typing import Tuple, List, Dict

class ElementFilterList:
    def __init__(self, lines : List[str]) -> None:
        self.rules = []
        for line in lines:
            self.addRule(line)

    def addRule(self, line : str):
        self.rules.append(line)

class ElementFilter:
    def setFilterList(self, filterList : Dict[str, ElementFilterList]) -> None:
        self.filterList = filterList 
        self.injections = {}

    def generateInjection(self, domain : str) -> bytes:
        if (domain in self.injections):
            return self.injections[domain]
        injection = b""
        if domain in self.filterList:
            for rule in self.filterList[domain].rules:
                injection += b"System.awaitHtmlElement(['"+ rule.encode("UTF-8") + b"'], System.removeHTMLElement);"
        self.injections[domain] = injection
        return injection
