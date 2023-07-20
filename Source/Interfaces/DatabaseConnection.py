from abc import ABC, abstractmethod
from typing import List
from Source.Book import Book


class DatabaseConnection(ABC):
    @abstractmethod
    def insertBooksIntoCatalogTable(self, books, booksToInsert):
        books += booksToInsert

    @abstractmethod
    def selectAll(self, books):
        books = sorted(books,
                            key=lambda book: book.title if "The" not in book.title[0:4]
                            else book.title[4:])
        return books

    @abstractmethod
    def select(self, searchTerm, books):
        return searchTerm if searchTerm in books else None

    @abstractmethod
    def delete(self, entry, books):
        books.remove(entry)

    @abstractmethod
    def deleteWhereTitle(self, title, books):
        deleted = 0
        for book in books:
            if title in book.title:
                books.remove(book)
                deleted += 1

        return deleted

    @abstractmethod
    def selectWith(self, bookDetail, books):
        found = []
        for book in books:
            if bookDetail in book.title or bookDetail in book.author:
                found.append(book)

        return sorted(found,
                      key=lambda book: book.title if "The" not in book.title[0:4]
                      else book.title[4:])

