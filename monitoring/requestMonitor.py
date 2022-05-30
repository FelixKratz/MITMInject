import flask
from monitoring.monitor import Monitor, HistoryElement

class RequestHistoryElement(HistoryElement):
    def __init__(self, request : flask.Request):
        super().__init__()
        self.baseURL = request.base_url
        self.url = request.url
        self.headers = request.headers
        self.clientIP = request.remote_addr
        self.request = request

    def __str__(self) -> str:
        return self.timeStamp + " -- " + self.clientIP + ": sent a request to " + self.baseURL

    def __repr__(self) -> str:
        return ""

class RequestMonitor(Monitor):
    def __init__(self):
        super().__init__()

    def monitor(self, request : flask.Request) -> None:
        self.addToHistory(RequestHistoryElement(request))