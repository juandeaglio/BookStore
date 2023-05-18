import unittest

from Source.StorageGateway import StorageGateway
from Source.InMemoryDatabase import InMemoryDatabase


class TestStorageGateway(unittest.TestCase):
    def setUp(self):
        self.books = [{'Title': 'The Hunger Games', 'Author': 'Suzanne Collins', 'Release year': '2012'},
                      {'Title': 'Harry Potter and the Sorcerer\'s Stone', 'Author': 'J.K. Rowling',
                       'Release year': '1998'},
                      {'Title': 'To Kill a Mockingbird', 'Author': 'Harper Lee', 'Release year': '1960'}]
        self.storageGateway = StorageGateway(InMemoryDatabase())
        self.storageGateway.save(self.books)

    def test_retrieveCatalog(self):
        numOfBooks = len(self.storageGateway.loadAllToCache())
        assert len(self.books) == numOfBooks

    def test_removeEntryFromCatalog(self):
        numOfBooks = len(self.storageGateway.loadAllToCache())
        self.storageGateway.removeEntry(self.books[len(self.books)-1])
        assert len(self.storageGateway.loadAllToCache()) == numOfBooks - 1

    def test_addEntryToCatalog(self):
        numOfBooks = len(self.storageGateway.loadAllToCache())
        self.storageGateway.add([{'Title': 'Catching Fire', 'Author': 'Suzanne Collins', 'Release year': '2009'}])
        assert len(self.storageGateway.loadAllToCache()) == numOfBooks + 1
