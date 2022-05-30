import gzip
import brotli
from typing import Tuple, List
import flask
import requests

class Content:
    def getRawContentInfo(headers : List[Tuple[str, str]]) -> Tuple[str, str]:
        contentType, encoding = "", ""
        i, encodingIndex = 0, -1
        for (name, value) in headers:
            if "content-type" == name.lower():
                contentType = value
            if "content-encoding" == name.lower():
                encoding = value
                encodingIndex = i
            i += 1
        return contentType, encoding, encodingIndex

    def decodeRawContent(content : bytes, encoding : str) -> bytes:
        if (encoding == "br"):
            return brotli.decompress(content)
        elif (encoding == "gzip"):
            return gzip.decompress(content)
        return content

    def encodeRawContent(content : bytes, encoding : str) -> bytes:
        if (encoding == "br"):
            return brotli.compress(content)
        elif (encoding == "gzip"):
            return gzip.compress(content)
        return content

    def getRequestHeadersFrom(request : flask.Request) -> dict:
        return dict(request.headers)

    def getResponseHeadersFrom(response : requests.Response) -> List[List[str]]:
        excluded_headers = ['transfer-encoding']
        return [[name, value] for (name, value) in response.raw.headers.items() if name.lower() not in excluded_headers]
