import re
from Source.Book import Book
from Source.Interfaces.DatabaseConnection import DatabaseConnection
import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('catalog.db')
        self.cursor = self.conn.cursor()
        self.initializeDatabase()
        self.sqlAdapter = SqlAdapter('catalog.db')

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

    def queryCatalogBySQL(self, query, data=None):
        if data is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)

        books = BookAdapter().getBooksChanged(self.commit())

        return books


class BookAdapter:
    @staticmethod
    def makeBookFromSQL(columns, row):
        book = Book()
        for i in range(len(columns)):
            setattr(book, columns[i][0], row[i])
        return book

    def getBooksChanged(self, sqlData):
        rows, columns = sqlData
        books = []
        for row in rows:
            book = self.makeBookFromSQL(columns, row)

            SqlAdapter('catalog.db').cleanDoubleQuotesFromTitle(book)
            books.append(book)
        return books


class SqlAdapter:
    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName)
        self.cursor = self.conn.cursor()

    def cleanDoubleQuotesFromTitle(self, book):
        # SQL requirement for quotes in field (must be double-quoted)
        if self.titleHasDoubleQuote(book):
            self.removeDuplicateQuotes(book)

    @staticmethod
    def removeDuplicateQuotes(book):
        book.title = re.sub("''+", "'", book.title)

    @staticmethod
    def titleHasDoubleQuote(book):
        return "\'\'" in book.title


class SqlBookDatabase(DatabaseConnection):
    def __init__(self):
        super().__init__()
        self.database = Database()

    def insertBooksIntoCatalogTable(self, books, booksToInsert):
        for book in booksToInsert:
            bookToInsert = self.replaceSingleQuoteWithDouble(book)
            self.insertQuery(bookToInsert.title, bookToInsert.author, bookToInsert.releaseYear)

        return super().insertBooksIntoCatalogTable(books, booksToInsert)

    def selectAll(self, books):
        return super().selectAll(books)

    def select(self, searchTerm, books):
        return super().select(searchTerm, books)

    def selectWith(self, bookDetail, books):
        return super().selectWith(bookDetail, books)

    def delete(self, entry, books):
        self.sendDeleteQuery(entry)
        return super().delete(entry, books)

    def deleteWhereTitle(self, title, books):
        self.sendDeleteWhereQuery(title)
        return super().deleteWhereTitle(title, books)

    def synchronize(self, books):
        sqlStatement = '''
                    SELECT title AS title, author AS author, releaseyear AS "releaseYear" FROM catalog ORDER BY title ASC
                '''
        return self.database.query(query=sqlStatement)

    def insertQuery(self, title, author, releaseYear):
        query = '''
                    INSERT INTO catalog (title, author, releaseyear)
                    VALUES (?, ?, ?)
                '''
        data = (title, author, releaseYear)
        self.database.query(query=query, data=data)

    def sendDeleteQuery(self, entry):
        parsedBook = self.replaceSingleQuoteWithDouble(entry)
        query = 'DELETE FROM catalog WHERE ' \
                'title LIKE \"%' + parsedBook.title + '%\" AND ' \
                                                      'author=\'' + parsedBook.author + '\' AND ' \
                                                                                        'releaseyear=\'' + parsedBook.releaseYear + '\''
        self.database.query(query=query)

    def sendDeleteWhereQuery(self, title):
        sanitizedDetail = self.replaceSingleQuoteWithDouble(title)
        query = 'DELETE FROM catalog WHERE title LIKE \"%' + sanitizedDetail + '%\"'
        self.database.query(query=query)

    def clearCatalog(self):
        self.database.dropTable('catalog')

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
