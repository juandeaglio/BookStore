from abc import ABC, abstractmethod
from typing import List
from Source.Book import Book


class DatabaseConnection(ABC):
    @abstractmethod
    def insertBooksIntoCatalogTable(self, booksToInsert):
        pass

    @abstractmethod
    def selectAll(self):
        pass

    @abstractmethod
    def select(self, searchTerm):
        pass

    @abstractmethod
    def delete(self, entry):
        pass
    @abstractmethod
    def deleteWhereTitle(self, title):
        pass

    @abstractmethod
    def selectWith(self, bookDetail):
        pass

    @abstractmethod
    def synchronize(self):
        pass

    @abstractmethod
    def selectFromAllFields(self, textContent):
        pass
