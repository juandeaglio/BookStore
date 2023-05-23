import unittest

from Source.Book import Book
from Source.BookStore import BookStore
from Source.InMemoryCatalog import InMemoryCatalog


class TestCatalog(unittest.TestCase):
    def setUp(self):
        self.books = [Book('The Hunger Games', 'Suzanne Collins', '2008'),
                      Book('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', '1998'),
                      Book('To Kill a Mockingbird', 'Harper Lee', '1960')]
        self.catalog = BookStore(InMemoryCatalog())

    def test_getAllBooksInCatalog(self):
        self.catalog.addToCatalog(self.books)
        assert len(self.catalog.getCatalog()) == len(self.books)

    def test_addBooksToCatalog(self):
        self.catalog.addToCatalog(self.books)
        assert len(self.catalog.getCatalog()) == 3

    def test_addDuplicateToCatalog(self):
        self.catalog.addToCatalog(self.books)
        self.catalog.addToCatalog([self.books[0]])
        assert len(self.catalog.getCatalog()) == 3

    def test_addNoBooksToCatalog(self):
        self.catalog.addToCatalog(None)
        assert len(self.catalog.getCatalog()) == 0

    def test_removeBookFromCatalogByName(self):
        self.catalog.addToCatalog(self.books)
        self.catalog.removeByTitle("Harry Potter")
        assert len(self.catalog.getCatalog()) == 2

    def test_catalogBooksAreSorted(self):
        self.catalog.addToCatalog(self.books)
        expectedSorted = [self.books[1], self.books[0], self.books[2]]
        assert expectedSorted == self.catalog.getCatalog()


if __name__ == '__main__':
    unittest.main()
