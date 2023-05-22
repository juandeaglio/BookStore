from Source.StorageGateway import StorageGateway


class CatalogInterface:
    def __init__(self, dbConnection):
        self.storageGateway = StorageGateway(dbConnection)

    def add(self, books):
        self.storageGateway.add(books)

    def removeAllByTitle(self, title):
        for book in self.getAllBooks():
            if title in book['Title']:
                self.storageGateway.removeEntryByTitle(title)

    def getAllBooks(self):
        return self.storageGateway.loadAllToCache()

    def getSizeOfCatalog(self):
        return len(self.getAllBooks())
