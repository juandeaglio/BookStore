from abc import ABC, abstractmethod


class StorageGatewayInterface(ABC):
    def __init__(self):
        self.data = []

    @abstractmethod
    def save(self, books):
        pass

    @abstractmethod
    def loadAll(self):
        pass

    @abstractmethod
    def loadEntry(self, book):
        pass

    def removeEntry(self, entry):
        if entry in self.data:
            self.data.remove(entry)

    def add(self, entries):
        for entry in entries:
            if entry not in self.data:
                self.data.append(entry)
