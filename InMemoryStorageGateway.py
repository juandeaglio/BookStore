from StorageGatewayInterface import StorageGatewayInterface


class InMemoryStorageGateway(StorageGatewayInterface):
    def __init__(self):
        self.data = []

    def save(self, books):
        self.data = books
        return False if self.data is None else True

    def load(self):
        return self.data

    def removeEntry(self, entry):
        if entry in self.data:
            self.data.remove(entry)
