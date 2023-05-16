import unittest

from BookStore import BookStore


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.books = [{'Title': 'The Hunger Games', 'Author': 'Suzanne Collins', 'Release year': '2012'},
                      {'Title': 'Harry Potter and the Sorcerer\'s Stone', 'Author': 'J.K. Rowling',
                       'Release year': '1998'},
                      {'Title': 'To Kill a Mockingbird', 'Author': 'Harper Lee', 'Release year': '1960'}]

    def test_addBookToCatalog(self):
        bookStore = BookStore()
        bookStore.addToCatalog(self.books)
        self.assertTrue(bookStore.catalog.size == 3)

    def test_addNoBooksToCatalog(self):
        bookStore = BookStore()
        bookStore.addToCatalog([])
        self.assertTrue(bookStore.catalog.size == 0)

    def test_removeBookFromCatalogByName(self):
        bookStore = BookStore()
        bookStore.addToCatalog(self.books)
        bookStore.removeByTitle("Harry Potter")
        self.assertTrue(bookStore.catalog.size == 2)

if __name__ == '__main__':
    unittest.main()
