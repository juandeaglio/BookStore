from Source.Interfaces.DatabaseConnection import DatabaseConnection


class StorageGateway:
    def __init__(self, dbConn):
        if isinstance(dbConn, DatabaseConnection):
            self.dbConnection = dbConn

    def fetchBooksFromDatabase(self):
        return self.dbConnection.selectAll()

    def loadEntryToCache(self, book):
        books = self.dbConnection.synchronize()
        return self.dbConnection.select(book)

    def removeEntry(self, entry):
        if self.doesBookExist(entry):
            books = self.dbConnection.synchronize()
            self.dbConnection.delete(entry)

    def add(self, entries):
        if entries is not None:
            if isinstance(entries, list):
                for entry in entries:
                    self.addUniqueEntry(entry)
            else:
                self.addUniqueEntry(entries)

    def addUniqueEntry(self, entry):
        books = self.dbConnection.synchronize()
        result = self.dbConnection.selectWith(entry.title)
        if not result:
            self.dbConnection.insertBooksIntoCatalogTable([entry])

    def doesBookExist(self, entry):
        return self.loadEntryToCache(entry) is not None

    def removeEntriesByTitle(self, title):
        books = self.loadEntryByTitleToCache(title)
        for book in books:
            self.removeEntry(book)

    def loadEntryByTitleToCache(self, title):
        books = self.dbConnection.synchronize()
        books = self.dbConnection.selectWith(title)
        return books

    def fetchByString(self, bookDetail):
        books = self.dbConnection.synchronize()
        books = self.dbConnection.selectWith(bookDetail)
        return books

    def fetchFromAllFields(self, textContent):
        self.dbConnection.synchronize()
        books = self.dbConnection.selectFromAllFields(textContent)
        return books
