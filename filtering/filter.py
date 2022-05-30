import flask
from typing import List, Tuple
from filtering.dnsFilter import DNSFilter
from filtering.pruneFilter import PruneFilter, PruneFilterList
from filtering.requestFilter import RequestFilter, RequestFilterList
from filtering.elementFilter import ElementFilter, ElementFilterList
from filtering.responseFilter import ResponseFilter, ResponseFilterList

class Filter:
    dnsFilter = DNSFilter()
    pruneFilter = PruneFilter()
    elementFilter = ElementFilter()
    requestFilter = RequestFilter()
    responseFilter = ResponseFilter()

    def blockResponse(statusCode = 404) -> flask.Response:
        resp = flask.Response(b"")
        resp.status_code = statusCode
        return resp

    def __init__(filterNames : List[str]) -> None:
        requestFilter, responseFilter, dnsFilter, elementFilter, pruneFilter = {}, {}, {}, {}, {}
        for filterName in filterNames:
            dnsFilter[filterName], requestFilter[filterName], responseFilter[filterName], elementFilter[filterName], pruneFilter[filterName] = Filter.loadAndCompileFilterList(filterName)

        Filter.dnsFilter.setFilterList(dnsFilter)
        Filter.pruneFilter.setFilterList(pruneFilter)
        Filter.elementFilter.setFilterList(elementFilter)
        Filter.requestFilter.setFilterList(requestFilter)
        Filter.responseFilter.setFilterList(responseFilter)

    def removeUnwantedLines(lines : List[str]) -> List[str]:
        return [line for line in lines if line != "" and not line.startswith("#")]

    def loadAndCompileFilterList(filterName : List[str]) -> Tuple[list, RequestFilterList, ResponseFilterList]:
        try:
            with open('filtering/lists/' + filterName + ".list") as f:
                dnsRange = [-1, -1]
                requestRange = [-1, -1]
                responseRange = [-1, -1]
                elementRange = [-1, -1]
                pruneRange = [-1, -1]
                print("Loading filter list with name: " + filterName)
                lines = Filter.removeUnwantedLines(f.read().splitlines())
                f.close()
                try:
                    dnsRange[0] = lines.index("[DNS]") + 1
                except ValueError:
                    print("No DNS filters present")

                try:
                    requestRange[0] = lines.index("[Request]") + 1
                    dnsRange[1] = requestRange[0] - 1
                except ValueError:
                    print("No Request filters present")
                
                try:
                    responseRange[0] = lines.index("[Response]") + 1
                    requestRange[1] = responseRange[0] - 1
                except ValueError:
                    print("No Response filters present")

                try:
                    elementRange[0] = lines.index("[Elements]") + 1
                    responseRange[1] = elementRange[0] - 1
                except ValueError:
                    print("No Element filters present")

                try:
                    pruneRange[0] = lines.index("[Prune]") + 1
                    elementRange[1] = pruneRange[0] - 1
                except ValueError:
                    print("No Prune rules present")

                pruneRange[1] = len(lines)
                if pruneRange[0] < 0:
                    elementRange[1] = pruneRange[1]
                if elementRange[0] < 0:
                    requestRange[1] = elementRange[1]
                if responseRange[0] < 0:
                    requestRange[1] = responseRange[1]
                if requestRange[0] < 0:
                    dnsRange[1] = requestRange[1]
                
                dnsList = lines[dnsRange[0]:dnsRange[1]] if dnsRange[0] >= 0 else []
                requestList = RequestFilterList(lines[requestRange[0]:requestRange[1]] if requestRange[0] >= 0 else [])
                responseList = ResponseFilterList(lines[responseRange[0]:responseRange[1]] if responseRange[0] >= 0 else [])
                elementList = ElementFilterList(lines[elementRange[0]:elementRange[1]] if elementRange[0] >= 0 else [])
                pruneList = PruneFilterList(lines[pruneRange[0]:pruneRange[1]] if pruneRange[0] >= 0 else [])
                return dnsList, requestList, responseList, elementList, pruneList
        except IOError:
            print("File not accessible")
        return [], RequestFilterList([]), ResponseFilterList([]), ElementFilterList([]), PruneFilterList([])