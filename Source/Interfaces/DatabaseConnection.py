from abc import ABC, abstractmethod
from typing import List
from Source.Book import Book


class DatabaseConnection(ABC):
    def __init__(self):
        self.books = []
    @abstractmethod
    def insertBooksIntoCatalogTable(self, books):
        oldLen = len(self.books)
        for book in books:
            self.books.append(book)

        if len(self.books) != oldLen:
            return self.books
        else:
            return None

    @abstractmethod
    def selectAll(self):
        self.books = sorted(self.books,
                            key=lambda book: book.title if "The" not in book.title[0:4]
                            else book.title[4:])
        return self.books

    @abstractmethod
    def select(self, searchTerm, books):
        return searchTerm if searchTerm in books else None

    @abstractmethod
    def delete(self, entry):
        self.books.remove(entry)

    @abstractmethod
    def deleteWhereTitle(self, title):
        deleted = 0
        for book in self.books:
            if title in book.title:
                self.books.remove(book)
                deleted += 1

        return deleted

    @abstractmethod
    def selectWith(self, bookDetail):
        found = []
        for book in self.books:
            if bookDetail in book.title or bookDetail in book.author:
                found.append(book)

        return sorted(found,
                      key=lambda book: book.title if "The" not in book.title[0:4]
                      else book.title[4:])

