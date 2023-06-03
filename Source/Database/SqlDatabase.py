import re

from Source.Book import Book
from Source.Interfaces.DatabaseConnection import DatabaseConnection
import sqlite3


class SqlAsBooks:
    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName)
        self.cursor = self.conn.cursor()

    def closeAndCommit(self):
        self.conn.commit()
        rows = self.cursor.fetchall()
        columns = self.cursor.description
        self.conn.close()
        return rows, columns

    def getBooksFromSqlQuery(self, query, data=None):
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
            book = Book()
            for i in range(len(columns)):
                setattr(book, columns[i][0], row[i])

            self.cleanDoubleQuotesFromTitle(book)
            books.append(book)
        return books

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
        sql = SqlAsBooks('catalog.db')
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS catalog (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                releaseyear TEXT
            )
        '''
        sql.getBooksFromSqlQuery(create_table_query)

    def selectAll(self):
        sql = SqlAsBooks('catalog.db')
        query = '''
                    SELECT title AS title, author AS author, releaseyear AS "releaseYear" FROM catalog ORDER BY title ASC
                '''
        return sql.getBooksFromSqlQuery(query)

    def delete(self, entry):
        pass

    def select(self, book):
        sql = SqlAsBooks('catalog.db')
        query = 'SELECT title AS title, author AS author, releaseyear AS "releaseYear" FROM catalog ' \
                'WHERE title=\'' + book.title + '\' AND author=\'' + book.author + '\' AND releaseyear=\'' \
                + book.releaseYear + '\''
        return sql.getBooksFromSqlQuery(query)

    def selectWhereTitle(self, title):
        pass

    def deleteWhereTitle(self, title):
        pass

    def insert(self, books):
        for book in books:
            self.insertQuery(book.title, book.author, book.releaseYear)

    def insertQuery(self, title, author, releaseYear):
        sql = SqlAsBooks('catalog.db')

        query = '''
                    INSERT INTO catalog (title, author, releaseyear)
                    VALUES (?, ?, ?)
                '''
        data = (title, author, releaseYear)
        sql.getBooksFromSqlQuery(query, data)

    def clearData(self):
        sql = SqlAsBooks('catalog.db')

        query = '''
                    DROP TABLE IF EXISTS catalog
                '''
        sql.getBooksFromSqlQuery(query)
        return self



