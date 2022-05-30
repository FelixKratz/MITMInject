from typing import List
from monitoring.client import Client

# Database implementation missing
class ClientHandler:
    def addClientToDatabase(client : Client) -> None:
        pass

    def loadClientsFromDatabase() -> List[Client]:
        return []

    def __init__(self):
        self.clients = ClientHandler.loadClientsFromDatabase()
        self.knownAddresses = [client.ipAddress for client in self.clients]

    def isKnownClient(self, ipAddress : str) -> bool:
        return True if ipAddress in self.knownAddresses else False
        
    def registerAsKnown(self, ipAddress : str) -> None:
        client = Client(ipAddress)
        self.clients.append(client)
        ClientHandler.addClientToDatabase(client)