import unittest
from Source.BookStore import BookStore
from Source.Catalog import Catalog
from Source.InMemoryDatabase import InMemoryDatabase


class TestBookStore(unittest.TestCase):
    def setUp(self):
        self.books = [{'Title': 'The Hunger Games', 'Author': 'Suzanne Collins', 'Release year': '2012'},
                      {'Title': 'Harry Potter and the Sorcerer\'s Stone', 'Author': 'J.K. Rowling',
                       'Release year': '1998'},
                      {'Title': 'To Kill a Mockingbird', 'Author': 'Harper Lee', 'Release year': '1960'}]
        catalog = Catalog(InMemoryDatabase())
        self.bookStore = BookStore(catalog)

    def test_getAllBooksInCatalog(self):
        self.bookStore.addToCatalog(self.books)
        assert len(self.bookStore.getCatalog()) == len(self.books)

    def test_addBookToCatalog(self):
        self.bookStore.addToCatalog(self.books)
        self.assertTrue(len(self.bookStore.getCatalog()) == 3)
        self.assertTrue('Harry' in self.bookStore.getCatalog()[0]['Title'])

    def test_addNoBooksToCatalog(self):
        self.bookStore.addToCatalog([])
        self.assertTrue(len(self.bookStore.getCatalog()) == 0)

    def test_removeBookFromCatalogByName(self):
        self.bookStore.addToCatalog(self.books)
        self.bookStore.removeByTitle("Harry Potter")
        self.assertTrue(len(self.bookStore.getCatalog()) == 2)

if __name__ == '__main__':
    unittest.main()
