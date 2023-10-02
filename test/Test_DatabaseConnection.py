import unittest

from Source.Book import Book
from Source.Database.InMemoryDatabase import InMemoryDatabase
from Source.Database.SqlBookDatabase import SqlBookDatabase
from Source.StorageGateway import StorageGateway
from test.BooksForTest import booksForTest


class TestInMemoryDatabase(unittest.TestCase):
    def setUp(self):
        self.books = booksForTest
        self.type = InMemoryDatabase
        self.storageGateway = StorageGateway(self.type())
        self.storageGateway.add(self.books)

    def test_persistenceWithSynchronize(self):
        self.newStorageGateway = StorageGateway(self.type())
        assert len(self.storageGateway.fetchBooksFromDatabase()) == len(self.books) + 1


class TestSqlDatabase(TestInMemoryDatabase):
    def setUp(self):
        super().setUp()
        self.books = booksForTest
        self.type = SqlBookDatabase
        self.storageGateway.dbConnection = self.type()
        self.storageGateway.add(self.books)
