import unittest

from Source.Book import Book
from Source.Catalog.InMemoryCatalog import InMemoryCatalog



class CatalogWithThreeBooks(unittest.TestCase):
    def setUp(self):
        self.books = [Book('The Hunger Games', 'Suzanne Collins', '2008'),
                      Book('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', '1998'),
                      Book('To Kill a Mockingbird', 'Harper Lee', '1960')]
        self.catalog = InMemoryCatalog()
        self.catalog.add(self.books)

    def test_getAllBooksInCatalog(self):
        assert len(self.catalog.getAllBooks()) == len(self.books)

    def test_getAllBooksInCatalogAsJson(self):
        assert len(self.catalog.getAllBooksJson()) == len(self.books)

    def test_addBooksToCatalog(self):
        assert self.catalog.getSizeOfCatalog() == 3

    def test_addDuplicateToCatalog(self):
        assert self.catalog.getSizeOfCatalog() == 3

    def test_removeBookFromCatalogByName(self):
        self.catalog.removeAllByTitle("Harry Potter")
        assert self.catalog.getSizeOfCatalog() == 2

    def test_catalogBooksAreSorted(self):
        expectedSorted = [self.books[1], self.books[0], self.books[2]]
        assert expectedSorted == self.catalog.getAllBooks()


class CatalogWithVariableAmountOfBooks(unittest.TestCase):
    def setUp(self):
        self.catalog = InMemoryCatalog()

    def test_addNoneToCatalog(self):
        self.catalog.add(None)
        assert self.catalog.getSizeOfCatalog() == 0

    def test_addNoBooksToCatalog(self):
        self.catalog.add([])
        assert self.catalog.getSizeOfCatalog() == 0

    def test_addSingleBookToCatalog(self):
        self.catalog.add(Book('The Hunger Games', 'Suzanne Collins', '2008'))
        assert self.catalog.getSizeOfCatalog() == 1


if __name__ == '__main__':
    unittest.main()
