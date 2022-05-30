import requests
from monitoring.monitor import Monitor, HistoryElement

class ResponseHistoryElement(HistoryElement):
    def __init__(self, response : requests.Response):
        super().__init__()
        self.response = response
        self.request = self.response.request
        self.baseURL = response.request.base_url
        self.url = response.request.url
        self.clientIP = response.request.remote_addr
    
    def __str__(self) -> str:
        return self.timeStamp + " -- " + self.clientIP + ": got a response from " + self.baseURL
    
    def __repr__(self) -> str:
        return ""

class ResponseMonitor(Monitor):
    def __init__(self):
        super().__init__()

    def monitor(self, response : requests.Response) -> None:
        self.addToHistory(ResponseHistoryElement(response))