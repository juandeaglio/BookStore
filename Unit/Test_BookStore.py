import unittest

from Source.BookStore import BookStore


class TestBookStore(unittest.TestCase):
    def setUp(self):
        self.books = [{'Title': 'The Hunger Games', 'Author': 'Suzanne Collins', 'Release year': '2012'},
                      {'Title': 'Harry Potter and the Sorcerer\'s Stone', 'Author': 'J.K. Rowling',
                       'Release year': '1998'},
                      {'Title': 'To Kill a Mockingbird', 'Author': 'Harper Lee', 'Release year': '1960'}]
        self.bookStore = BookStore()

    def test_getAllBooksInCatalog(self):
        self.bookStore.addToCatalog(self.books)
        assert len(self.bookStore.getCatalog()) == len(self.books)

    def test_addBookToCatalog(self):
        self.bookStore.addToCatalog(self.books)
        self.assertTrue(self.bookStore.catalog.size == 3)

    def test_addNoBooksToCatalog(self):
        self.bookStore.addToCatalog([])
        self.assertTrue(self.bookStore.catalog.size == 0)

    def test_removeBookFromCatalogByName(self):
        self.bookStore.addToCatalog(self.books)
        self.bookStore.removeByTitle("Harry Potter")
        self.assertTrue(self.bookStore.catalog.size == 2)

if __name__ == '__main__':
    unittest.main()
