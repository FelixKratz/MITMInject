import uuid
from typing import Optional
# Clients should be stored in database...

class Client:
    def __init__(self, ipAddress : str = "", uuid : Optional[str] = None):
        self.uuid = uuid
        self.ipAddress = ipAddress