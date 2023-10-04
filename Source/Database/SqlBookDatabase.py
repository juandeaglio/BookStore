from Source.Book import Book
from Source.Database.InMemoryDatabase import InMemoryDatabase
from Source.Database.Utilities import *
from Source.Interfaces.DatabaseConnection import DatabaseConnection
import sqlite3


class Database:
    catalog_table_name = 'catalog'

    def __init__(self):
        self.conn = sqlite3.connect('catalog.db')
        self.cursor = self.conn.cursor()
        self.initialize_database()

    def initialize_database(self):
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS catalog (
                id INTEGER PRIMARY KEY,
                {0}
        '''
        create_table_query = create_table_query.format(' TEXT, '.join(Book().attributes))
        create_table_query += ' TEXT)'
        self.query(query=create_table_query)

    def drop_catalog(self, name):
        query = "DROP TABLE IF EXISTS " + self.catalog_table_name
        self.query(query=query)

    def query(self, query, data=None):
        if data is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)

        books = get_books_changed(self.commit())

        return books

    def commit(self):
        self.conn.commit()
        rows = self.cursor.fetchall()
        columns = self.cursor.description
        return rows, columns

    def get_books_from_executed_sql(self, query, data=None):
        if data is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)

        books = get_books_changed(self.commit())

        return books

    def get_all_books_from_catalog(self):
        sql_statement = 'SELECT * FROM catalog'
        return self.get_books_from_executed_sql(sql_statement)

    def insert_query(self, book):
        query = '''
                    INSERT INTO catalog ({0})
                    VALUES ({1})
                '''
        query = query.format(', '.join(book.attributes), ', '.join(['?'] * len(book.attributes)))
        data = tuple(getattr(book, attr) for attr in book.attributes)
        self.query(query=query, data=data)

    def send_delete_query(self, entry):
        parsed_book = replace_single_quote_with_double(entry)
        query = '''DELETE FROM catalog WHERE
                title LIKE ? 
                AND author = ? 
                AND releaseyear = ?'''
        data = ('%' + parsed_book.title + '%', parsed_book.author, parsed_book.releaseYear)
        self.query(query=query, data=data)

    def send_delete_where_query(self, title):
        sanitized_detail = replace_single_quote_with_double(title)
        query = 'DELETE FROM catalog WHERE title LIKE ?'
        data = ('%' + sanitized_detail + '%',)
        self.query(query=query, data=data)


class SqlBookDatabase(DatabaseConnection):
    def __init__(self):
        super().__init__()
        self.cached_data = InMemoryDatabase()
        self.database = Database()

    def insert_books_into_catalog_table(self, books_to_insert):
        for book in books_to_insert:
            book_to_insert = replace_single_quote_with_double(book)
            self.database.insert_query(book_to_insert)

        return self.cached_data.insert_books_into_catalog_table(books_to_insert)

    def select_all(self):
        self.synchronize()
        return self.cached_data.select_all()

    def select(self, search_term):
        return self.cached_data.select(search_term)

    def select_with_substring(self, book_detail):
        return self.cached_data.select_with_substring(book_detail)

    def select_from_title_or_author(self, book_detail):
        return self.cached_data.select_from_title_or_author(book_detail)

    def delete(self, entry):
        self.database.send_delete_query(entry)
        return self.cached_data.delete(entry)

    def delete_where_title(self, title):
        self.database.send_delete_where_query(title)
        return self.cached_data.delete_where_title(title)

    def synchronize(self):
        self.cached_data.books = self.database.get_all_books_from_catalog()
        return self.cached_data.books

    def clear_catalog(self):
        self.database.drop_catalog('catalog')

    def delete_sqlite(self):
        import os
        os.remove('db.sqlite3')

    def select_from_all_fields(self, text_content):
        return self.cached_data.select_from_all_fields(text_content)
