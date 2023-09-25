from Source.Interfaces.DatabaseConnection import DatabaseConnection


class StorageGateway:
    def __init__(self, dbConn):
        self.books = []
        if isinstance(dbConn, DatabaseConnection):
            self.dbConnection = dbConn

    def fetchBooksFromDatabase(self):
        self.books = self.dbConnection.synchronize(self.books)
        self.books = self.dbConnection.selectAll(self.books)
        return self.books

    def loadEntryToCache(self, book):
        self.books = self.dbConnection.synchronize(self.books)
        return self.dbConnection.select(book, self.books)

    def removeEntry(self, entry):
        if self.doesBookExist(entry):
            self.books = self.dbConnection.synchronize(self.books)
            self.dbConnection.delete(entry, self.books)

    def add(self, entries):
        if entries is not None:
            if isinstance(entries, list):
                for entry in entries:
                    self.addUniqueEntry(entry)
            else:
                self.addUniqueEntry(entries)

    def addUniqueEntry(self, entry):
        self.books = self.dbConnection.synchronize(self.books)
        result = self.dbConnection.selectWith(entry.title, self.books)
        if not result:
            self.dbConnection.insertBooksIntoCatalogTable(self.books, [entry])

    def doesBookExist(self, entry):
        return self.loadEntryToCache(entry) is not None

    def removeEntriesByTitle(self, title):
        books = self.loadEntryByTitleToCache(title)
        for book in books:
            self.removeEntry(book)

    def loadEntryByTitleToCache(self, title):
        self.books = self.dbConnection.synchronize(self.books)
        books = self.dbConnection.selectWith(title, self.books)
        return books

    def fetchByString(self, bookDetail):
        self.books = self.dbConnection.synchronize(self.books)
        books = self.dbConnection.selectWith(bookDetail, self.books)
        return books

    def fetchFromAllFields(self, textContent):
        self.books = self.dbConnection.synchronize(self.books)
        books = self.dbConnection.selectFromAllFields(textContent, self.books)
        return books
