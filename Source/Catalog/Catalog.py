from Source.Book import Book
from Source.StorageGateway import StorageGateway


class Catalog:
    def __init__(self, dbConnection=None):
        self.storageGateway = StorageGateway(dbConnection)

    def add(self, books):
        if isinstance(books, Book):
            self.storageGateway.addUniqueEntry(books)
        else:
            self.storageGateway.add(books)

    def removeAllByTitle(self, title):
        self.storageGateway.removeEntriesByTitle(title)

    def getAllBooks(self):
        return self.storageGateway.fetchBooksFromDatabase()

    def getSizeOfCatalog(self):
        return len(self.getAllBooks())

    def toString(self):
        catalog = ''
        for book in self.getAllBooks():
            catalog += book.title + "," + book.author + "," + book.releaseYear + '\n'

        return catalog

    def getAllBooksJson(self):
        jsonList = []
        for book in self.getAllBooks():
            jsonList.append(book.to_json())

        return jsonList

    def search(self, bookDetail):
        return self.storageGateway.fetchByString(bookDetail)
