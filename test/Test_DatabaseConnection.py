import multiprocessing
import unittest

from Source.Book import Book
from Source.Database.InMemoryDatabase import InMemoryDatabase
from Source.Database.SqlBookDatabase import SqlBookDatabase
from Source.StorageGateway import StorageGateway
from test.BooksForTest import booksForTest
from test.FakedOSLibrary import FakedOSLibrary
from test.FakedProcessLibrary import FakedProcessLibrary
from test.FakeProcess import FakeProcess


def worker(type, returnDict):
    new_gw = StorageGateway(type())
    new_gw.add(Book(title="Harry Potter", author="JK Rowling", releaseYear="2001", imagePath="SomePath",
                    description="SomeDescription", price="SomePrice"))
    returnDict[0] = new_gw.fetchBooksFromDatabase()

class TestInMemoryDatabase(unittest.TestCase):
    def setUp(self):
        self.books = booksForTest
        self.type = InMemoryDatabase
        self.storageGateway = StorageGateway(self.type())
        self.storageGateway.add(self.books)
        self.processLibrary = FakedProcessLibrary()

    def test_persistenceWithSynchronize(self):
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        p = multiprocessing.Process(target=worker, args=(self.type, return_dict))
        p.start()
        p.join()
        retVals = return_dict.values()
        # no persistence with in-memory db.
        assert len(retVals) == 1


class TestSqlDatabase(unittest.TestCase):
    def setUp(self):
        self.books = booksForTest
        self.type = SqlBookDatabase
        SqlBookDatabase().clearCatalog()
        self.storageGateway = StorageGateway(self.type())

        self.storageGateway.add(self.books)
        self.processLibrary = FakedProcessLibrary()

    def test_persistenceWithSynchronize(self):
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        p = multiprocessing.Process(target=worker, args=(self.type, return_dict))
        p.start()
        p.join()
        retVals = return_dict.values()
        # persistence with sqlite db.
        assert len(retVals[0]) == 6

