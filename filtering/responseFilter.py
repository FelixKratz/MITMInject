import os
import ast
import numpy as np
import regex as re
from config import Config
from networking.contentActions import Content
from typing import ByteString, Tuple, Dict, List

class ResponseFilterRule:
    replaceReg = re.compile(r"replace\((.+?)\)$")
    def __init__(self):
        pass

    def process(self, content : str) -> str:
        pass

class ResponseReplaceRule(ResponseFilterRule):
    def __init__(self, replaceNew : str, replaceRule : str) -> None:
        self.reg = re.compile(replaceRule.encode('UTF-8'))
        self.replaceNew = replaceNew.encode('UTF-8')
    
    def process(self, content : str) -> str:
        return re.sub(self.reg, self.replaceNew, content)


class ResponseFilterList:
    def interpretString(string : str) -> ResponseFilterRule:
        # Replace detection
        replaceMatches = re.findall(ResponseFilterRule.replaceReg, string)
        rules = []
        for replaceMatch in replaceMatches:
            replaceRule, replaceNew = ast.literal_eval(replaceMatch)
            rules.append(ResponseReplaceRule(replaceNew, replaceRule))

        # Add new rule detection here
        return rules

    def __init__(self, lines : List[str]) -> None:
        self.rules = []
        self.filterRules = []
        for line in lines:
            self.addLine(line)

    def addLine(self, line : str) -> None:
        lineComponents = []
        if " " in line:
            lineComponents = line.split(" ")
        else: 
            lineComponents = [line, Config.DEFAUT_RESPONSE_RULE]
        
        siteRule = re.compile(lineComponents[0])
        filterRule = ResponseFilterList.interpretString(" ".join(lineComponents[1:]))
        self.rules.append(siteRule)
        self.filterRules.append(filterRule)

class ResponseFilter:
    def filterWithRules(content : str, rules : List[ResponseFilterRule]) -> str:
        for rule in rules:
            content = rule.process(content)
        return content

    def setFilterList(self, filterList : Dict[str, ResponseFilterList]) -> None:
        self.filterList = filterList 

    def filter(self, site : str, domain : str, headers : dict, content : bytes) -> Tuple[dict, bytes, bool]:
        _, encoding, encodingIndex = Content.getRawContentInfo(headers)
        if (not domain in self.filterList):
            return headers, content, False

        siteMatches = np.array([re.match(rule, site) for rule in self.filterList[domain].rules])
        whereAbouts = np.where(siteMatches)[0] 
        matchIndex = whereAbouts[0] if len(whereAbouts) > 0 else None 

        if not matchIndex:
            return headers, content, False    

        # Filtering
        content = Content.decodeRawContent(content, encoding)
        content = ResponseFilter.filterWithRules(content, self.filterList[domain].filterRules[matchIndex])
        if Config.RECOMPRESS_JS:
            content = Content.encodeRawContent(content, encoding)
        elif encodingIndex > 0:
            headers.pop(encodingIndex)
            
        return headers, content, False