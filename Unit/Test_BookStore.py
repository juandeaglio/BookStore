import unittest
from Source.BookStore import BookStore
from Source.TestCatalog import TestCatalog


class TestBookStore(unittest.TestCase):
    def setUp(self):
        self.books = [{'Title': 'The Hunger Games', 'Author': 'Suzanne Collins', 'Release year': '2012'},
                      {'Title': 'Harry Potter and the Sorcerer\'s Stone', 'Author': 'J.K. Rowling',
                       'Release year': '1998'},
                      {'Title': 'To Kill a Mockingbird', 'Author': 'Harper Lee', 'Release year': '1960'}]
        self.bookStore = BookStore(TestCatalog())

    def test_getAllBooksInCatalog(self):
        self.bookStore.addToCatalog(self.books)
        assert len(self.bookStore.getCatalog()) == len(self.books)

    def test_addBooksToCatalog(self):
        self.bookStore.addToCatalog(self.books)
        assert len(self.bookStore.getCatalog()) == 3

    def test_addNoBooksToCatalog(self):
        self.bookStore.addToCatalog(None)
        assert len(self.bookStore.getCatalog()) == 0

    def test_removeBookFromCatalogByName(self):
        self.bookStore.addToCatalog(self.books)
        self.bookStore.removeByTitle("Harry Potter")
        assert len(self.bookStore.getCatalog()) == 2

    def test_catalogBooksAreSorted(self):
        self.bookStore.addToCatalog(self.books)
        expectedSorted = [self.books[1], self.books[0], self.books[2]]
        assert expectedSorted == self.bookStore.getCatalog()


if __name__ == '__main__':
    unittest.main()
