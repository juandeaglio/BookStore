from Source.StorageGateway import StorageGateway


class Catalog:
    def __init__(self, dbConnection=None):
        self.storageGateway = StorageGateway(dbConnection)

    def add(self, books):
        self.storageGateway.add(books)

    def removeAllByTitle(self, title):
        self.storageGateway.removeEntryByTitle(title)

    def getAllBooks(self):
        return self.storageGateway.fetchBooksFromDatabase()

    def getSizeOfCatalog(self):
        return len(self.getAllBooks())

    def toString(self):
        catalog = ''
        for book in self.getAllBooks():
            catalog += book.title + ", " + book.author + ", " + book.releaseYear + '\n'

        return catalog