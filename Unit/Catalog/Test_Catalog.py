import unittest

from Source.Book import Book
from Source.BookStore import BookStore
from Source.Catalog.InMemoryCatalog import InMemoryCatalog


class TestCatalog(unittest.TestCase):
    def setUp(self):
        self.books = [Book('The Hunger Games', 'Suzanne Collins', '2008'),
                      Book('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', '1998'),
                      Book('To Kill a Mockingbird', 'Harper Lee', '1960')]
        self.catalog = InMemoryCatalog()

    def test_getAllBooksInCatalog(self):
        self.catalog.add(self.books)
        assert len(self.catalog.getAllBooks()) == len(self.books)

    def test_addBooksToCatalog(self):
        self.catalog.add(self.books)
        assert len(self.catalog.getAllBooks()) == 3

    def test_addDuplicateToCatalog(self):
        self.catalog.add(self.books)
        self.catalog.add([self.books[0]])
        assert len(self.catalog.getAllBooks()) == 3

    def test_addNoneToCatalog(self):
        self.catalog.add(None)
        assert len(self.catalog.getAllBooks()) == 0

    def test_addNoBooksToCatalog(self):
        self.catalog.add([])
        assert len(self.catalog.getAllBooks()) == 0

    def test_removeBookFromCatalogByName(self):
        self.catalog.add(self.books)
        self.catalog.removeAllByTitle("Harry Potter")
        assert len(self.catalog.getAllBooks()) == 2

    def test_removeExtraQuotesWhenGettingCatalog(self):
        self.catalog.add(self.books+[Book("Harry''s Potter", "J.K. Rowling", "1999")])
        assert self.catalog.getAllBooks()[1].title == "Harry's Potter"

    def test_catalogBooksAreSorted(self):
        self.catalog.add(self.books)
        expectedSorted = [self.books[1], self.books[0], self.books[2]]
        assert expectedSorted == self.catalog.getAllBooks()


if __name__ == '__main__':
    unittest.main()
