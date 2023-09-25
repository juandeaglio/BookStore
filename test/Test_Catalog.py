import unittest

from Source.Book import Book
from Source.Catalog.InMemoryCatalog import InMemoryCatalog
from Source.Catalog.PersistentCatalog import PersistentCatalog
from Source.Database.SqlBookDatabase import SqlBookDatabase
from test.BooksForTest import booksForTest


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
        self.books = booksForTest
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
        assert len(self.catalog.booksToJson(self.catalog.getAllBooks())) == len(self.books)

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
        for book in actualBooks:
            print("actual")
            print(book.toString())
        expectedBooks = []

        for book in self.books:
            if title in book.title:
                print ("expected")
                expectedBooks.append(book)
                print(book.toString())
        expectedBooks.sort(key=lambda x: x.title)
        assert expectedBooks == actualBooks

    def test_fetchBooksWithEmptyFields(self):
        self.catalog.add([Book("Harry Cotter", "", "", "", "")])
        result = self.catalog.fetchBooksWithEmptyFields()
        assert len(result) == 1


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
        self.catalog.add(booksForTest[0])
        assert self.catalog.getSizeOfCatalog() == 1


class PersistentCatalogWithVariableAmountOfBooks(CatalogWithVariableAmountOfBooks):
    def setUp(self):
        SqlBookDatabase().clearCatalog()
        super().setUp()
        self.catalog = PersistentCatalog()

if __name__ == '__main__':
    unittest.main()
