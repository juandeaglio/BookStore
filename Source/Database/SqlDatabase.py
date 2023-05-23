from Source.Book import Book
from Source.Interfaces.DatabaseConnection import DatabaseConnection
import sqlite3


class Sql:
    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName)
        self.cursor = self.conn.cursor()

    def closeAndCommit(self):
        self.conn.commit()
        rows = self.cursor.fetchall()
        columns = self.cursor.description
        self.conn.close()
        return rows, columns

    def executeCommit(self, query):
        self.cursor.execute(query)
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
        sql = Sql('catalog.db')
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS catalog (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                releaseyear TEXT
            )
        '''
        sql.cursor.execute(create_table_query)
        sql.closeAndCommit()

    def selectAll(self):
        sql = Sql('catalog.db')
        query = '''
                    SELECT title AS title, author AS author, releaseyear AS "releaseYear" FROM catalog ORDER BY title ASC
                '''
        return sql.executeCommit(query)

    def delete(self, entry):
        pass

    def select(self, book):
        sql = Sql('catalog.db')
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
            print("the book: " + str(book))
            self.insertQuery(book.title, book.author, book.releaseYear)

    def insertQuery(self, title, author, releaseYear):
        sql = Sql('catalog.db')

        query = '''
                    INSERT INTO catalog (title, author, releaseyear)
                    VALUES (?, ?, ?)
                '''
        data = (title, author, releaseYear)

        sql.cursor.execute(query, data)
        sql.closeAndCommit()

    def clearData(self):
        sql = Sql('catalog.db')

        query = '''
                    DROP TABLE IF EXISTS catalog
                '''
        sql.executeCommit(query)
        return self
