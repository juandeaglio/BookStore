from Source.RestMessage import RestMessage
from Source.SimpleSocketServer import SimpleSocketServer
import threading
from abc import ABC, abstractmethod


class RestGateway(ABC):
    def __init__(self):
        pass

    def listens(self):
        pass

    def getMessageFromQueue(self):
        pass

    def hasConnection(self):
        pass

    def closeConnection(self):
        pass

    def parseMessage(self, message):
        pass

    @abstractmethod
    def send(self):
        pass
