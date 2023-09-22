import unittest
from operator import eq

from Source.Book import Book
from Source.StorageGateway import StorageGateway
from Source.Database.InMemoryDatabase import InMemoryDatabase
from Source.Database.SqlBookDatabase import SqlBookDatabase
from test.BooksForTest import booksForTest


class TestInMemoryStorageGateway(unittest.TestCase):
    def setUp(self):
        self.books = booksForTest
        self.storageGateway = StorageGateway(InMemoryDatabase())
        self.storageGateway.add(self.books)

    def test_retrieveCatalog(self):
        assert len(self.books) == len(self.storageGateway.fetchBooksFromDatabase())

    def test_removeEntryFromCatalog(self):
        expectedTotal = len(self.storageGateway.fetchBooksFromDatabase()) - 1
        self.storageGateway.removeEntry(self.books[len(self.books) - 1])
        assert len(self.storageGateway.fetchBooksFromDatabase()) == expectedTotal

    def test_addEntryToCatalog(self):
        expectedTotal = len(self.storageGateway.fetchBooksFromDatabase()) + 1
        self.storageGateway.add([Book('Catching Fire', 'Suzanne Collins', '2009')])
        assert len(self.storageGateway.fetchBooksFromDatabase()) == expectedTotal

    def test_addDuplicateEntryToCatalog(self):
        expectedTotal = len(self.storageGateway.fetchBooksFromDatabase())
        books = booksForTest
        self.storageGateway.add(Book(title=books[0].title, author=books[0].author, releaseYear=books[0].releaseYear, imagePath="SomePath", description="SomeDescription"))
        assert len(self.storageGateway.fetchBooksFromDatabase()) == expectedTotal

    def test_addNothing(self):
        expectedTotal = len(self.books)
        self.storageGateway.add(None)
        assert len(self.storageGateway.fetchBooksFromDatabase()) == expectedTotal

    def test_searchBooks(self):
        title = "Harry Potter"
        expected = []
        for book in self.books:
            if title in book.title:
                expected.append(book)
        expected.sort(key=lambda x: x.title)
        assert self.storageGateway.fetchByString(title) == expected


class TestPersistentStorageGateway(TestInMemoryStorageGateway):
    def setUp(self):
        self.books = booksForTest
        SqlBookDatabase().clearCatalog()
        self.storageGateway = StorageGateway(SqlBookDatabase())
        self.storageGateway.add(self.books)

    # Removed SQL injection tests for add & delete methods using "; DROP TABLE catalog;--" since they
    # passed initially and added no further testing value.
