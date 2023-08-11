import re
from Source.Book import Book
from Source.Database.InMemoryDatabase import InMemoryDatabase
from Source.Interfaces.InMemoryBooks import InMemoryBooks
import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('catalog.db')
        self.cursor = self.conn.cursor()
        self.initializeDatabase()
        self.sqlAdapter = SqlAdapter()

    def initializeDatabase(self):
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS catalog (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                releaseyear TEXT
            )
        '''
        self.query(query=create_table_query)

    def dropTable(self, name):
        query = "DROP TABLE IF EXISTS " + name
        self.query(query=query)

    def query(self, query, data=None):
        if data is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)

        books = BookAdapter().getBooksChanged(self.commit())

        return books

    def commit(self):
        self.conn.commit()
        rows = self.cursor.fetchall()
        columns = self.cursor.description
        return rows, columns


class BookAdapter:
    @staticmethod
    def makeBookFromSQL(columns, row):
        book = Book()
        for i in range(len(columns)):
            setattr(book, columns[i][0], row[i])
        return book

    @staticmethod
    def getBooksChanged(sqlData):
        rows, columns = sqlData
        books = []
        for row in rows:
            book = BookAdapter.makeBookFromSQL(columns, row)

            SqlAdapter().cleanDoubleQuotesFromTitle(book)
            books.append(book)
        return books

    @staticmethod
    def replaceSingleQuoteWithDouble(entry):
        # SQL requirement for single quote character ' in field.
        newEntry = Book()
        if isinstance(entry, str):
            newEntry = re.sub("'", "''", entry)

        else:
            newEntry.author = entry.author
            newEntry.releaseYear = entry.releaseYear
            newEntry.title = entry.title

            if "'" in newEntry.title and "''" not in newEntry.title:
                title = re.sub("'", "''", newEntry.title)
                newEntry.title = title

        return newEntry


class SqlAdapter:
    @staticmethod
    def cleanDoubleQuotesFromTitle(book):
        # SQL requirement for quotes in field (must be double-quoted)
        if SqlAdapter.titleHasDoubleQuote(book):
            SqlAdapter.removeDuplicateQuotes(book)

    @staticmethod
    def removeDuplicateQuotes(book):
        book.title = re.sub("''+", "'", book.title)

    @staticmethod
    def titleHasDoubleQuote(book):
        return "\'\'" in book.title


class SqlInMemoryBooks(InMemoryBooks):
    def __init__(self):
        super().__init__()
        self.cachedData = InMemoryDatabase()
        self.database = Database()

    def insertBooksIntoCatalogTable(self, books, booksToInsert):
        for book in booksToInsert:
            bookToInsert = BookAdapter().replaceSingleQuoteWithDouble(book)
            self.insertQuery(bookToInsert.title, bookToInsert.author, bookToInsert.releaseYear)

        return self.cachedData.insertBooksIntoCatalogTable(books, booksToInsert)

    def selectAll(self, books):
        return self.cachedData.selectAll(books)

    def select(self, searchTerm, books):
        return self.cachedData.select(searchTerm, books)

    def selectWith(self, bookDetail, books):
        return self.cachedData.selectWith(bookDetail, books)

    def delete(self, entry, books):
        self.sendDeleteQuery(entry)
        return self.cachedData.delete(entry, books)

    def deleteWhereTitle(self, title, books):
        self.sendDeleteWhereQuery(title)
        return self.cachedData.deleteWhereTitle(title, books)

    def insertQuery(self, title, author, releaseYear):
        query = '''
                    INSERT INTO catalog (title, author, releaseyear)
                    VALUES (?, ?, ?)
                '''
        data = (title, author, releaseYear)
        self.database.query(query=query, data=data)

    def sendDeleteQuery(self, entry):
        parsedBook = BookAdapter().replaceSingleQuoteWithDouble(entry)
        query = 'DELETE FROM catalog WHERE ' \
                'title LIKE \"%' + parsedBook.title + '%\" AND ' \
                'author=\'' + parsedBook.author + '\' AND ' \
                'releaseyear=\'' + parsedBook.releaseYear + '\''
        self.database.query(query=query)

    def sendDeleteWhereQuery(self, title):
        sanitizedDetail = BookAdapter().replaceSingleQuoteWithDouble(title)
        query = 'DELETE FROM catalog WHERE title LIKE \"%' + sanitizedDetail + '%\"'
        self.database.query(query=query)

    def clearCatalog(self):
        self.database.dropTable('catalog')
