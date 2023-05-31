import re

from Source.Interfaces.DatabaseConnection import DatabaseConnection


class StorageGateway:
    def __init__(self, databasePipe):
        self.data = []
        if isinstance(databasePipe, DatabaseConnection):
            self.dbConnection = databasePipe

    def save(self, books):
        self.data = self.dbConnection.insert(books)
        return False if self.data is None else True

    def loadAllToCache(self):
        books = self.dbConnection.selectAll()
        for book in books:
            self.cleanDoubleQuotesFromTitle(book)
        return books

    def cleanDoubleQuotesFromTitle(self, book):
        # SQL requirement for quotes in field (must be double-quoted)
        if "\'\'" in book.title:
            book.title = re.sub("''+", "'", book.title)

    def loadEntryToCache(self, book):
        return self.dbConnection.select(book)

    def removeEntry(self, entry):
        if self.doesBookExist(entry):
            self.dbConnection.delete(entry)

    def add(self, entries):
        for entry in entries:
            self.replaceSingleQuoteWithDouble(entry)
            self.addUniqueEntry(entry)

    def addUniqueEntry(self, entry):
        if not self.dbConnection.select(entry):
            self.dbConnection.insert([entry])

    def replaceSingleQuoteWithDouble(self, entry):
        # SQL requirement for quotes in field.
        if "'" in entry.title:
            entry.title = re.sub("'", "''", entry.title)

    def doesBookExist(self, entry):
        return self.loadEntryToCache(entry) is not None

    def removeEntryByTitle(self, title):
        self.removeEntry(self.loadEntryByTitleToCache(title))

    def doesTitleExist(self, title):
        return self.loadEntryByTitleToCache(title) is not None

    def loadEntryByTitleToCache(self, title):
        book = self.dbConnection.deleteWhereTitle(title)
        return book
