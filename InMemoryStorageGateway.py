from StorageGateway import StorageGateway


class InMemoryStorageGateway(StorageGateway):
    def __init__(self):
        self.data = None

    def save(self, books):
        self.data = books

    def load(self):
        return self.data
