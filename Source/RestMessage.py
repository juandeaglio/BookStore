from abc import ABC,abstractmethod


class RestMessage(ABC):
    @abstractmethod
    def __init__(self, method=None, path=None, body=None, rawMsg=None):
        self.method = method
        self.path = path
        self.body = body
        self.rawMsg = rawMsg

    def __eq__(self, other):
        return True


class GetCatalogRestMessage:
    def toBytes(self):
        pass