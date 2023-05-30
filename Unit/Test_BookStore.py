import unittest

from Source.Book import Book
from Source.BookStore import BookStore
from Source.Catalog.InMemoryCatalog import InMemoryCatalog


class BookStoreTestCase(unittest.TestCase):
    def test_createBookStoreWithCatalog(self):
        self.bookStore = BookStore(InMemoryCatalog())
        self.bookStore.addToCatalog([Book(title="Harry Potter 1", author="J.K. Rowling", releaseYear=2001)])
        assert len(self.bookStore.getCatalog()) > 0


if __name__ == '__main__':
    unittest.main()
