import json

from Source.Book import Book


class TestBook:
    def test_bookToJson(self):
        newBook = Book('The Hunger Games', 'Suzanne Collins', '2008')
        jsonBook = newBook.to_json()
        assert Book(jsonBook['title'], jsonBook['author'], jsonBook['releaseYear']) == newBook
