from Source.RestMessage import RestMessage
from Source.SimpleSocketServer import SimpleSocketServer
import threading
from abc import ABC, abstractmethod


class RestGateway(ABC):
    def __init__(self):
        self.client = None
        self.connection = SimpleSocketServer()

    def listens(self):
        self.client = threading.Thread(target=self.connection.listen)

    def getMessageFromQueue(self):
        parsedMessage = self.parseMessage(self.connection.receive())
        return parsedMessage

    def hasConnection(self):
        return True

    def closeConnection(self):
        pass

    def parseMessage(self, message):
        return message

    @abstractmethod
    def send(self):
        pass
