import unittest
from operator import eq

from Source.Book import Book
from Source.StorageGateway import StorageGateway
from Source.Database.InMemoryDatabase import InMemoryDatabase
from Source.Database.SqlDatabase import SqlDatabase


class TestInMemoryStorageGateway(unittest.TestCase):
    def setUp(self):
        self.books = [Book('The Hunger Games', 'Suzanne Collins', '2008'),
                      Book('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', '1998'),
                      Book('To Kill a Mockingbird', 'Harper Lee', '1960')]
        self.storageGateway = StorageGateway(InMemoryDatabase())
        self.storageGateway.add(self.books)

    def test_retrieveCatalog(self):
        expectedTotal = len(self.storageGateway.fetchBooksFromDatabase())
        assert len(self.books) == expectedTotal

    def test_removeEntryFromCatalog(self):
        expectedTotal = len(self.storageGateway.fetchBooksFromDatabase()) - 1
        self.storageGateway.removeEntry(self.books[len(self.books)-1])
        assert len(self.storageGateway.fetchBooksFromDatabase()) == expectedTotal

    def test_addEntryToCatalog(self):
        expectedTotal = len(self.storageGateway.fetchBooksFromDatabase()) + 1
        self.storageGateway.add([Book('Catching Fire', 'Suzanne Collins', '2009')])
        assert len(self.storageGateway.fetchBooksFromDatabase()) == expectedTotal

    def test_addDuplicateEntryToCatalog(self):
        expectedTotal = len(self.storageGateway.fetchBooksFromDatabase())
        books = [Book('The Hunger Games', 'Suzanne Collins', '2008'),
                 Book('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', '1998'),
                 Book('To Kill a Mockingbird', 'Harper Lee', '1960')]
        self.storageGateway.add(books)
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


class TestPersistentStorageGateway(unittest.TestCase):
    def setUp(self):
        self.books = [Book('The Hunger Games', 'Suzanne Collins', '2008'),
                      Book('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', '1998'),
                      Book('To Kill a Mockingbird', 'Harper Lee', '1960')]
        SqlDatabase().clearData()
        self.storageGateway = StorageGateway(SqlDatabase())
        self.storageGateway.add(self.books)

    def test_retrieveCatalog(self):
        self.books.sort(key=lambda x: x.title)
        actual = self.storageGateway.fetchBooksFromDatabase()
        assert eq(self.books, actual)

    def test_addEntryToCatalog(self):
        expectedTotal = len(self.storageGateway.fetchBooksFromDatabase()) + 1
        self.storageGateway.add([Book('Catching Fire', 'Suzanne Collins', '2009')])
        assert len(self.storageGateway.fetchBooksFromDatabase()) == expectedTotal

    def test_addDuplicateEntryToCatalog(self):
        expectedTotal = len(self.storageGateway.fetchBooksFromDatabase())
        self.storageGateway.add(self.books)
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
        actual = self.storageGateway.fetchByString(title)
        assert eq(actual, expected)
