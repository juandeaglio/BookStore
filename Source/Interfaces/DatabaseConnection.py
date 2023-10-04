from abc import ABC, abstractmethod
from typing import List
from Source.Book import Book


class DatabaseConnection(ABC):
    @abstractmethod
    def insert_books_into_catalog_table(self, books_to_insert):
        pass

    @abstractmethod
    def select_all(self):
        pass

    @abstractmethod
    def select(self, search_term):
        pass

    @abstractmethod
    def delete(self, entry):
        pass
    @abstractmethod
    def delete_where_title(self, title):
        pass

    @abstractmethod
    def select_with_substring(self, book_detail):
        pass

    @abstractmethod
    def synchronize(self):
        pass

    @abstractmethod
    def select_from_all_fields(self, text_content):
        pass

    @abstractmethod
    def select_from_title_or_author(self, title):
        pass
