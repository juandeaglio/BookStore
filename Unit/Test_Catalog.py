import unittest

from Source.Book import Book
from Source.Catalog.InMemoryCatalog import InMemoryCatalog


def sortBooksByTitle(books):
    titles = arrayFromTitles(books)
    titles.sort()
    return titles


def createListOfTitles(books):
    titles = arrayFromTitles(books)
    return titles


def arrayFromTitles(books):
    titles = []
    for book in books:
        titles.append(book.title)
    return titles


class CatalogWithInitialAmountOfBooks(unittest.TestCase):
    def setUp(self):
        self.books = [Book('The Hunger Games', 'Suzanne Collins', '2008'),
                      Book('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', '1998'),
                      Book('Harry Potter and the Chamber of Secrets', 'J.K. Rowling', '1999'),
                      Book('Harry Potter and the Prisoner of Azkaban', 'J.K. Rowling', '1999'),
                      Book('To Kill a Mockingbird', 'Harper Lee', '1960')]
        self.catalog = InMemoryCatalog()
        self.catalog.add(self.books)

    def test_getAllBooksInCatalog(self):
        assert len(self.catalog.getAllBooks()) == len(self.books)

    def test_getAllBooksInCatalogAsJson(self):
        assert len(self.catalog.getAllBooksJson()) == len(self.books)

    def test_addBooksToCatalog(self):
        assert self.catalog.getSizeOfCatalog() == len(self.books)

    def test_addDuplicateToCatalog(self):
        assert self.catalog.getSizeOfCatalog() == len(self.books)

    def test_removeBookFromCatalogByName(self):
        oldLength = self.catalog.getSizeOfCatalog()
        self.catalog.removeAllByTitle("Harry Potter")
        assert self.catalog.getSizeOfCatalog() == oldLength - 1

    def test_catalogBooksAreSorted(self):
        expectedSortOrder = sortBooksByTitle(self.books)
        actualSortOrder = createListOfTitles(self.catalog.getAllBooks())
        assert expectedSortOrder == actualSortOrder

    def test_search_books(self):
            assert False


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
