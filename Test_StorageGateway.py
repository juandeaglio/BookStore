import unittest

from InMemoryStorageGateway import InMemoryStorageGateway


class TestStorageGateway(unittest.TestCase):
    def setUp(self):
        self.books = [{'Title': 'The Hunger Games', 'Author': 'Suzanne Collins', 'Release year': '2012'},
                      {'Title': 'Harry Potter and the Sorcerer\'s Stone', 'Author': 'J.K. Rowling',
                       'Release year': '1998'},
                      {'Title': 'To Kill a Mockingbird', 'Author': 'Harper Lee', 'Release year': '1960'}]
        self.storageGateway = InMemoryStorageGateway()

    def test_saveAndRetrieveCatalog(self):
        assert self.storageGateway.save(self.books)
        numOfBooks = len(self.storageGateway.loadAll())
        assert len(self.books) == numOfBooks

    def test_removeEntryFromCatalog(self):
        self.storageGateway.save(self.books)
        numOfBooks = len(self.storageGateway.loadAll())
        self.storageGateway.removeEntry(self.books[len(self.books)-1])
        assert len(self.storageGateway.loadAll()) == numOfBooks - 1

    def test_addEntryToCatalog(self):
        self.storageGateway.save(self.books)
        numOfBooks = len(self.storageGateway.loadAll())
        self.storageGateway.add([{'Title': 'Catching Fire', 'Author': 'Suzanne Collins', 'Release year': '2009'}])
        assert len(self.storageGateway.loadAll()) == numOfBooks + 1
