import json

from Source.Book import Book
from test.BooksForTest import booksForTest

class TestBook:
    def test_bookToJson(self):
        book = booksForTest[0]
        jsonBook = book.to_json()
        otherBook = Book()
        for attribute in book.attributes:
            otherBook.__setattr__(attribute, jsonBook[attribute])

        assert book.to_json() == otherBook.to_json()