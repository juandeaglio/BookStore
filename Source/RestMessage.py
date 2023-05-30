from abc import ABC,abstractmethod


class RestMessage(ABC):
    @abstractmethod
    def __init__(self, method=None, path=None, body=None, rawMsg=None):
        self.method = method
        self.path = path
        self.body = body
        self.rawMsg = rawMsg

    @abstractmethod
    def toBytes(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    def endHTTPMessage(self, paramaters=''):
        return 'HTTP/1.1\r\n\r\n'