from Source.Book import Book
from Source.Database.InMemoryDatabase import InMemoryDatabase
from Source.Database.Utilities import *
from Source.Interfaces.DatabaseConnection import DatabaseConnection
import sqlite3


class Database:
    catalogTableName = 'catalog'

    def __init__(self):
        self.conn = sqlite3.connect('catalog.db')
        self.cursor = self.conn.cursor()
        self.initializeDatabase()

    def initializeDatabase(self):
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS catalog (
                id INTEGER PRIMARY KEY,
                {0}
        '''
        create_table_query = create_table_query.format(' TEXT, '.join(Book().attributes))
        create_table_query += ' TEXT)'
        self.query(query=create_table_query)

    def dropCatalog(self, name):
        query = "DROP TABLE IF EXISTS " + self.catalogTableName
        self.query(query=query)

    def query(self, query, data=None):
        if data is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)

        books = getBooksChanged(self.commit())

        return books

    def commit(self):
        self.conn.commit()
        rows = self.cursor.fetchall()
        columns = self.cursor.description
        return rows, columns

    def getBooksFromExecutedSQL(self, query, data=None):
        if data is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)

        books = getBooksChanged(self.commit())

        return books

    def getAllBooksFromCatalog(self):
        sqlStatement = 'SELECT * FROM catalog'
        return self.getBooksFromExecutedSQL(sqlStatement)

    def insertQuery(self, book):
        query = '''
                    INSERT INTO catalog ({0})
                    VALUES ({1})
                '''
        query = query.format(', '.join(book.attributes), ', '.join(['?'] * len(book.attributes)))
        data = tuple(getattr(book, attr) for attr in book.attributes)
        self.query(query=query, data=data)

    def sendDeleteQuery(self, entry):
        parsedBook = replaceSingleQuoteWithDouble(entry)
        query = '''DELETE FROM catalog WHERE
                title LIKE ? 
                AND author = ? 
                AND releaseyear = ?'''
        data = ('%' + parsedBook.title + '%', parsedBook.author, parsedBook.releaseYear)
        self.query(query=query, data=data)

    def sendDeleteWhereQuery(self, title):
        sanitizedDetail = replaceSingleQuoteWithDouble(title)
        query = 'DELETE FROM catalog WHERE title LIKE ?'
        data = ('%' + sanitizedDetail + '%',)
        self.query(query=query, data=data)


class SqlBookDatabase(DatabaseConnection):
    def __init__(self):
        super().__init__()
        self.books = []
        self.cachedData = InMemoryDatabase()
        self.database = Database()

    def insertBooksIntoCatalogTable(self, booksToInsert):
        for book in booksToInsert:
            bookToInsert = replaceSingleQuoteWithDouble(book)
            self.database.insertQuery(bookToInsert)

        return self.cachedData.insertBooksIntoCatalogTable(booksToInsert)

    def selectAll(self):
        self.synchronize()
        return self.cachedData.selectAll()

    def select(self, searchTerm):
        return self.cachedData.select(searchTerm)

    def selectWith(self, bookDetail):
        return self.cachedData.selectWith(bookDetail)

    def delete(self, entry):
        self.database.sendDeleteQuery(entry)
        return self.cachedData.delete(entry)

    def deleteWhereTitle(self, title):
        self.database.sendDeleteWhereQuery(title)
        return self.cachedData.deleteWhereTitle(title)

    def synchronize(self):
        return self.database.getAllBooksFromCatalog()

    def clearCatalog(self):
        self.database.dropCatalog('catalog')

    def deleteSqlite(self):
        import os
        os.remove('db.sqlite3')

    def selectFromAllFields(self, textContent):
        return self.cachedData.selectFromAllFields(textContent)
