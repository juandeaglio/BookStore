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
        super().__init__()
        self.initializeDatabase()
        self.databaseToCache()

    def databaseToCache(self):
        database = BooksToSql('catalog.db')
        sqlStatement = '''
                    SELECT title AS title, author AS author, releaseyear AS "releaseYear" FROM catalog ORDER BY title ASC
                '''
        self.books = self.query(database=database, query=sqlStatement)

    def query(self, database, query, data=None):
        if data is None:
            self.books = database.queryCatalogBySQL(query)
        else:
            self.books = database.queryCatalogBySQL(query=query, data=data)

        return self.books

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
        self.query(database=database, query=create_table_query)

    def selectAll(self):
        self.databaseToCache()
        return super().selectAll()

    def select(self, searchTerm, books):
        database = BooksToSql('catalog.db')
        parsedBook = self.replaceSingleQuoteWithDouble(searchTerm)
        query = 'SELECT title AS title, author AS author, releaseyear AS "releaseYear" FROM catalog ' \
                'WHERE title LIKE \"%' + parsedBook.title + '%\" AND author=\'' + parsedBook.author + \
                '\' AND releaseyear=\'' \
                + parsedBook.releaseYear + '\''

        return self.query(database=database, query=query)

    def insertBooksIntoCatalogTable(self, books):
        for book in books:
            bookToInsert = self.replaceSingleQuoteWithDouble(book)
            self.insertQuery(bookToInsert.title, bookToInsert.author, bookToInsert.releaseYear)

    def replaceSingleQuoteWithDouble(self, entry):
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

    def insertQuery(self, title, author, releaseYear):
        database = BooksToSql('catalog.db')

        query = '''
                    INSERT INTO catalog (title, author, releaseyear)
                    VALUES (?, ?, ?)
                '''
        data = (title, author, releaseYear)
        self.query(database=database, query=query, data=data)

    def clearData(self):
        database = BooksToSql('catalog.db')

        query = '''
                    DROP TABLE IF EXISTS catalog
                '''
        self.query(database, query)

    def selectWith(self, bookDetail):
        database = BooksToSql('catalog.db')
        sanitizedDetail = self.replaceSingleQuoteWithDouble(bookDetail)
        query = 'SELECT title AS title, author AS author, releaseyear AS "releaseYear" FROM catalog ' \
                'WHERE title LIKE \"%' + sanitizedDetail + '%\" OR author=\'' + sanitizedDetail + '\' ORDER by title'

        return self.query(database=database, query=query)

    def delete(self, entry):
        database = BooksToSql('catalog.db')
        parsedBook = self.replaceSingleQuoteWithDouble(entry)
        query = 'DELETE FROM catalog WHERE ' \
                'title LIKE \"%' + parsedBook.title + '%\" AND ' \
                'author=\'' + parsedBook.author + '\' AND ' \
                'releaseyear=\'' + parsedBook.releaseYear + '\''

        return self.query(database=database, query=query)

    def deleteWhereTitle(self, title):
        database = BooksToSql('catalog.db')
        sanitizedDetail = self.replaceSingleQuoteWithDouble(title)
        query = 'DELETE FROM catalog WHERE title LIKE \"%' + sanitizedDetail + '%\"'

        return self.query(database=database, query=query)