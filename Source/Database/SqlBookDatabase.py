import re
from Source.Book import Book
from Source.Database.InMemoryDatabase import InMemoryDatabase
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

        books = BookAdapter().getBooksChanged(self.commit())

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

        books = BookAdapter().getBooksChanged(self.commit())

        return books

    def getAllBooksFromCatalog(self):
        sqlStatement = 'SELECT {0} FROM catalog'
        sqlStatement = sqlStatement.format(', '.join(Book().attributes))
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
        parsedBook = BookAdapter().replaceSingleQuoteWithDouble(entry)
        query = '''DELETE FROM catalog WHERE
                title LIKE ? 
                AND author = ? 
                AND releaseyear = ?'''
        data = ('%' + parsedBook.title + '%', parsedBook.author, parsedBook.releaseYear)
        self.query(query=query, data=data)

    def sendDeleteWhereQuery(self, title):
        sanitizedDetail = BookAdapter().replaceSingleQuoteWithDouble(title)
        query = 'DELETE FROM catalog WHERE title LIKE ?'
        data = ('%' + sanitizedDetail + '%',)
        self.query(query=query, data=data)


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

            BookAdapter.cleanDoubleQuotesFromTitle(book)
            books.append(book)
        return books

    @staticmethod
    def replaceSingleQuoteWithDouble(entry):
        # SQL requirement for single quote character ' in field.
        newEntry = Book()
        if isinstance(entry, str):
            newEntry = re.sub("'", "''", entry)

        else:
            for attribute in entry.attributes:
                #check if the entry.attribute has a single quote
                if "'" in getattr(entry, attribute):
                    setattr(newEntry, attribute, re.sub("'", "''", getattr(entry, attribute)))
                else:
                    setattr(newEntry, attribute, getattr(entry, attribute))

        return newEntry

    @staticmethod
    def cleanDoubleQuotesFromTitle(book):
        # SQL requirement for quotes in field (must be double-quoted)
        BookAdapter.removeDuplicateQuotes(book)

    @staticmethod
    def removeDuplicateQuotes(book):
        for attribute in book.attributes:
            setattr(book, attribute, re.sub("''", "'", getattr(book, attribute)))

    @staticmethod
    def titleHasDoubleQuote(book):
        return "\'\'" in book.title


class SqlBookDatabase(DatabaseConnection):

    def __init__(self):
        super().__init__()
        self.cachedData = InMemoryDatabase()
        self.database = Database()

    def insertBooksIntoCatalogTable(self, books, booksToInsert):
        for book in booksToInsert:
            bookToInsert = BookAdapter().replaceSingleQuoteWithDouble(book)
            self.database.insertQuery(bookToInsert)

        return self.cachedData.insertBooksIntoCatalogTable(books, booksToInsert)

    def selectAll(self, books):
        return self.cachedData.selectAll(books)

    def select(self, searchTerm, books):
        return self.cachedData.select(searchTerm, books)

    def selectWith(self, bookDetail, books):
        return self.cachedData.selectWith(bookDetail, books)

    def delete(self, entry, books):
        self.database.sendDeleteQuery(entry)
        return self.cachedData.delete(entry, books)

    def deleteWhereTitle(self, title, books):
        self.database.sendDeleteWhereQuery(title)
        return self.cachedData.deleteWhereTitle(title, books)

    def synchronize(self, books):
        return self.cachedData.synchronize(self.database.getAllBooksFromCatalog())

    def clearCatalog(self):
        self.database.dropCatalog('catalog')

    def deleteSqlite(self):
        import os
        os.remove('db.sqlite3')

    def selectFromAllFields(self, textContent, books):
        return self.cachedData.selectFromAllFields(textContent, books)