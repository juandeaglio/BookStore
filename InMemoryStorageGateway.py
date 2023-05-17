from StorageGatewayInterface import StorageGatewayInterface


class InMemoryStorageGateway(StorageGatewayInterface):

    def save(self, books):
        self.data = books
        return False if self.data is None else True

    def loadAllToCache(self):
        return self.data

    def loadEntryToCache(self, book):
        return book if book in self.data else None


