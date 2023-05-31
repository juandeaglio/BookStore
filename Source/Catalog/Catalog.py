from Source.StorageGateway import StorageGateway


class Catalog:
    def __init__(self, dbConnection=None):
        self.storageGateway = StorageGateway(dbConnection)

    def add(self, books):
        if books is not None and len(books) > 0:
            self.storageGateway.add(books)

    def removeAllByTitle(self, title):
        for book in self.getAllBooks():
            if title in book.title:
                self.storageGateway.removeEntryByTitle(title)

    def getAllBooks(self):
        return self.storageGateway.loadAllToCache()

    def getSizeOfCatalog(self):
        return len(self.getAllBooks())

    def toString(self):
        catalog = ''
        for book in self.getAllBooks():
            catalog += book.title + ", " + book.author + ", " + book.releaseYear + '\n'

        return catalog
