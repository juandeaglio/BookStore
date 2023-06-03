import re

from Source.Book import Book
from Source.Interfaces.DatabaseConnection import DatabaseConnection
import sqlite3


class BooksToSql:
    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName)
        self.cursor = self.conn.cursor()

    def closeAndCommit(self):
        self.conn.commit()
        rows = self.cursor.fetchall()
        columns = self.cursor.description
        self.conn.close()
        return rows, columns

    def queryCatalogBySQL(self, query, data=None):
        if data is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)

        books = self.getBooksChanged()

        return books

    def getBooksChanged(self):
        rows, columns = self.closeAndCommit()
        books = []
        for row in rows:
            book = self.makeBookFromSQL(columns, row)

            self.cleanDoubleQuotesFromTitle(book)
            books.append(book)
        return books

    def makeBookFromSQL(self, columns, row):
        book = Book()
        for i in range(len(columns)):
            setattr(book, columns[i][0], row[i])
        return book

    def cleanDoubleQuotesFromTitle(self, book):
        # SQL requirement for quotes in field (must be double-quoted)
        if self.titleHasDoubleQuote(book):
            self.removeDuplicateQuotes(book)

    def removeDuplicateQuotes(self, book):
        book.title = re.sub("''+", "'", book.title)

    def titleHasDoubleQuote(self, book):
        return "\'\'" in book.title


class SqlDatabase(DatabaseConnection):
    def __init__(self):
        self.initializeDatabase()

    def initializeDatabase(self):
        database = BooksToSql('catalog.db')
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS catalog (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                releaseyear TEXT
            )
        '''
        database.queryCatalogBySQL(create_table_query)

    def selectAll(self):
        database = BooksToSql('catalog.db')
        query = '''
                    SELECT title AS title, author AS author, releaseyear AS "releaseYear" FROM catalog ORDER BY title ASC
                '''
        return database.queryCatalogBySQL(query)

    def select(self, book):
        database = BooksToSql('catalog.db')
        query = 'SELECT title AS title, author AS author, releaseyear AS "releaseYear" FROM catalog ' \
                'WHERE title=\'' + book.title + '\' AND author=\'' + book.author + '\' AND releaseyear=\'' \
                + book.releaseYear + '\''
        return database.queryCatalogBySQL(query)

    def insertBooksIntoCatalogTable(self, books):
        for book in books:
            self.replaceSingleQuoteWithDouble(book)
            self.insertQuery(book.title, book.author, book.releaseYear)

    def replaceSingleQuoteWithDouble(self, entry):
        # SQL requirement for single quote character ' in field.
        if "'" in entry.title:
            entry.title = re.sub("'", "''", entry.title)

    def insertQuery(self, title, author, releaseYear):
        database = BooksToSql('catalog.db')

        query = '''
                    INSERT INTO catalog (title, author, releaseyear)
                    VALUES (?, ?, ?)
                '''
        data = (title, author, releaseYear)
        database.queryCatalogBySQL(query, data)

    def clearData(self):
        database = BooksToSql('catalog.db')

        query = '''
                    DROP TABLE IF EXISTS catalog
                '''
        database.queryCatalogBySQL(query)



