import unittest

from Source.Book import Book
from Source.Catalog.InMemoryCatalog import InMemoryCatalog
from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlBookDatabase import SqlBookDatabase


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

    def test_smokeTestOfAllFunctions(self):
        title = "Harry"
        sizeOfSearch = len(self.catalog.search(title))
        if self.catalog.getSizeOfCatalog() - sizeOfSearch == len(self.books) - sizeOfSearch:
            books = self.catalog.getAllBooks()
            length = len(books)
            for i in range(0, length):
                self.catalog.removeAllByTitle(books.pop().title)

        assert self.catalog.getSizeOfCatalog() == 0

    def test_getAllBooksJson(self):
        assert len(self.catalog.getAllBooksJson()) == len(self.books)

    def test_removeBookFromCatalogByName(self):
        oldLength = self.catalog.getSizeOfCatalog()
        self.catalog.removeAllByTitle("Harry Potter")
        assert self.catalog.getSizeOfCatalog() < oldLength

    def test_catalogBooksAreSorted(self):
        expectedSortOrder = sortBooksByTitle(self.books)
        actualSortOrder = createListOfTitles(self.catalog.getAllBooks())
        assert expectedSortOrder == actualSortOrder

    def test_searchBooks(self):
        title = "Harry Potter"
        actualBooks = self.catalog.search(title)
        expectedBooks = []

        for book in self.books:
            if title in book.title:
                expectedBooks.append(book)
        expectedBooks.sort(key=lambda x: x.title)
        assert expectedBooks == actualBooks


class PersistentCatalogWithInitialAmountOfBooks(CatalogWithInitialAmountOfBooks):
    def setUp(self):
        SqlBookDatabase().clearCatalog()
        super().setUp()
        self.catalog = PersistentCatalog()
        self.catalog.add(self.books)


class CatalogWithVariableAmountOfBooks(unittest.TestCase):
    def setUp(self):
        self.catalog = InMemoryCatalog()

    def test_addNoneToCatalog(self):
        self.catalog.add(None)
        expectedSize = self.catalog.getSizeOfCatalog()
        assert expectedSize == 0

    def test_addNoBooksToCatalog(self):
        self.catalog.add([])
        assert self.catalog.getSizeOfCatalog() == 0

    def test_addSingleBookToCatalog(self):
        self.catalog.add(Book('The Hunger Games', 'Suzanne Collins', '2008'))
        assert self.catalog.getSizeOfCatalog() == 1


class PersistentCatalogWithVariableAmountOfBooks(CatalogWithVariableAmountOfBooks):
    def setUp(self):
        SqlBookDatabase().clearCatalog()
        super().setUp()
        self.catalog = PersistentCatalog()

if __name__ == '__main__':
    unittest.main()
