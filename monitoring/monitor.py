import time
from config import Config
from os import linesep as endl
from monitoring.client import Client

class HistoryElement:
    def __init__(self):
        self.timeStamp = str(time.time())
    
class Monitor:
    def __init__(self):
        self.history = []

    def addToHistory(historyElement : HistoryElement) -> None:
        self.history.append(historyElement)
        if len(self.history) > Config.MAX_HISTORY_LEN:
            self.history.pop(0)

    def logHistoryToFile(file : str) -> None:
        with open(file, "rw") as f:
            for h in self.history:
                f.write(str(h) + endl)
            f.close()