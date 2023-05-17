from abc import ABC, abstractmethod


class StorageGatewayInterface(ABC):
    def __init__(self):
        self.data = []

    @abstractmethod
    def save(self, books):
        pass

    @abstractmethod
    def loadAllToCache(self):
        pass

    @abstractmethod
    def loadEntryToCache(self, book):
        pass

    def removeEntry(self, entry):
        if entry in self.data:
            self.data.remove(entry)

    def add(self, entries):
        for entry in entries:
            if not self.doesBookExist(entry):
                self.data.append(entry)

    def doesBookExist(self, entry):
        return self.loadEntryToCache(entry) is not None
