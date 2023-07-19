from abc import ABC, abstractmethod
from typing import List
from Source.Book import Book


class DatabaseConnection(ABC):
    def __init__(self):
        self.books = []
    @abstractmethod
    def insertBooksIntoCatalogTable(self, books):
        pass

    @abstractmethod
    def selectAll(self):
        self.books = sorted(self.books,
                            key=lambda book: book.title if "The" not in book.title[0:4]
                            else book.title[4:])
        return self.books

    @abstractmethod
    def select(self, searchTerm):
        for book in self.books:
            if book == searchTerm:
                return book


    @abstractmethod
    def delete(self, entry):
        pass

    @abstractmethod
    def deleteWhereTitle(self, title):
        pass

    @abstractmethod
    def selectWith(self, bookDetail):
        pass
