from Source.Book import Book
from Source.Interfaces.DatabaseConnection import DatabaseConnection
import sqlite3


class Connection:
    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName)
        self.cursor = self.conn.cursor()

    def closeAndCommit(self):
        self.conn.commit()
        rows = self.cursor.fetchall()
        columns = self.cursor.description
        self.conn.close()
        return rows, columns

    def executeCommit(self, query, data=None):
        if data is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)
        rows, columns = self.closeAndCommit()

        books = []
        for row in rows:
            book = Book()
            for i in range(len(columns)):
                setattr(book, columns[i][0], row[i])
            books.append(book)

        return books


class SqlDatabase(DatabaseConnection):
    def __init__(self):
        self.initializeDatabase()

    def initializeDatabase(self):
        sql = Connection('catalog.db')
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS catalog (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                releaseyear TEXT
            )
        '''
        sql.executeCommit(create_table_query)

    def selectAll(self):
        sql = Connection('catalog.db')
        query = '''
                    SELECT title AS title, author AS author, releaseyear AS "releaseYear" FROM catalog ORDER BY title ASC
                '''
        return sql.executeCommit(query)

    def delete(self, entry):
        pass

    def select(self, book):
        sql = Connection('catalog.db')
        query = 'SELECT title AS title, author AS author, releaseyear AS "releaseYear" FROM catalog ' \
                'WHERE title=\'' + book.title + '\' AND author=\'' + book.author + '\' AND releaseyear=\'' \
                + book.releaseYear + '\''
        return sql.executeCommit(query)

    def selectWhereTitle(self, title):
        pass

    def deleteWhereTitle(self, title):
        pass

    def insert(self, books):
        for book in books:
            self.insertQuery(book.title, book.author, book.releaseYear)

    def insertQuery(self, title, author, releaseYear):
        sql = Connection('catalog.db')

        query = '''
                    INSERT INTO catalog (title, author, releaseyear)
                    VALUES (?, ?, ?)
                '''
        data = (title, author, releaseYear)
        sql.executeCommit(query, data)

    def clearData(self):
        sql = Connection('catalog.db')

        query = '''
                    DROP TABLE IF EXISTS catalog
                '''
        sql.executeCommit(query)
        return self
