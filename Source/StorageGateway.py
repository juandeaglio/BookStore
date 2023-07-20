from Source.Interfaces.DatabaseConnection import DatabaseConnection


class StorageGateway:
    def __init__(self, dbConn):
        self.books = []
        if isinstance(dbConn, DatabaseConnection):
            self.dbConnection = dbConn

    def fetchBooksFromDatabase(self):
        self.books = self.dbConnection.selectAll(self.books)
        return self.books

    def loadEntryToCache(self, book):
        return self.dbConnection.select(book, self.books)

    def removeEntry(self, entry):
        if self.doesBookExist(entry):
            self.dbConnection.delete(entry, self.books)

    def add(self, entries):
        if entries is not None:
            for entry in entries:
                self.addUniqueEntry(entry)

    def addUniqueEntry(self, entry):
        result = self.dbConnection.select(entry, self.books)
        if not result:
            self.dbConnection.insertBooksIntoCatalogTable(self.books, [entry])

    def doesBookExist(self, entry):
        return self.loadEntryToCache(entry) is not None

    def removeEntryByTitle(self, title):
        self.removeEntry(self.loadEntryByTitleToCache(title))

    def loadEntryByTitleToCache(self, title):
        books = self.dbConnection.deleteWhereTitle(title, self.books)
        return books

    def fetchByString(self, bookDetail):
        books = self.dbConnection.selectWith(bookDetail, self.books)
        return books
