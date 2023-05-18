from Source.DatabaseConnection import DatabaseConnection


class StorageGateway:
    def __init__(self, databasePipe):
        self.data = []
        if isinstance(databasePipe, DatabaseConnection):
            self.dbConnection = databasePipe

    def save(self, books):
        self.data = self.dbConnection.insert(books)
        return False if self.data is None else True

    def loadAllToCache(self):
        return self.dbConnection.selectAll()

    def loadEntryToCache(self, book):
        return self.dbConnection.select(book)

    def removeEntry(self, entry):
        if self.doesBookExist(entry):
            self.dbConnection.delete(entry)

    def add(self, entries):
        for entry in entries:
            if not self.dbConnection.select(entry):
                self.dbConnection.insert([entry])

    def doesBookExist(self, entry):
        return self.loadEntryToCache(entry) is not None
