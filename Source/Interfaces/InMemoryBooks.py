from abc import ABC, abstractmethod
from typing import List
from Source.Book import Book


class InMemoryBooks(ABC):
    @abstractmethod
    def insertBooksIntoCatalogTable(self, books, booksToInsert):
        pass

    @abstractmethod
    def selectAll(self, books):
        pass

    @abstractmethod
    def select(self, searchTerm, books):
        pass

    @abstractmethod
    def delete(self, entry, books):
        pass
    @abstractmethod
    def deleteWhereTitle(self, title, books):
        pass

    @abstractmethod
    def selectWith(self, bookDetail, books):
        pass

