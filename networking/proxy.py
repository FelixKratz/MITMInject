import flask
import requests
from typing import List
from config import Config
from flask import Response
from filtering.filter import Filter
from networking.injection import Injection
from networking.contentActions import Content
from monitoring.__init__ import responseMonitor, requestMonitor

class Proxy:
    # Gets the original site with a modified request, returns the modified response
    def getSite(site : str, domain : str, request : flask.Request) -> flask.Response:

        # Request blocking/altering
        request, blocked = Filter.requestFilter.filter(request, site, domain)
        if blocked:
            return Filter.blockResponse()

        # Monitor Requests        
        if Config.MONITOR_REQUESTS:
            requestMonitor.monitor(request)

        # Get the original site 
        headers = Content.getRequestHeadersFrom(request)
        response = requests.request(request.method, site, stream=True, timeout=3,
                                params=request.args, json=request.json,
                                headers=headers, allow_redirects=False,
                                data=request.form)
        # Alter the original site
        alteredResponse = Proxy.alterResponse(response, site.split("://")[1], domain)
        
        # Monitor Responses
        if Config.MONITOR_RESPONSES:
            responseMonitor.monitor(alteredResponse) 
        
        return alteredResponse

    # Performs the Website filtering/altering and injection
    def alterResponse(response : requests.Response, site : str, domain : str) -> flask.Response:
        headers = Content.getResponseHeadersFrom(response)
        rawContent = response.raw.read(decode_content=False)
        
        # Response filtering and altering
        headers, rawContent, blocked = Filter.responseFilter.filter(site, domain, headers, rawContent)
        if blocked:
            return Filter.blockResponse()

        # Content Injection
        headers, rawContent = Injection.injectInto(site, domain, headers, rawContent)
        out = Response(rawContent, headers=headers)
        out.status_code = response.status_code
        return out