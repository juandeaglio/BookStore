from Source.DatabaseConnection import DatabaseConnection


class InMemoryDatabase(DatabaseConnection):
    def __init__(self):
        self.books = []

    def insert(self, books):
        for book in books:
            if book not in self.books:
                self.books.append(book)

    def selectAll(self):
        return self.books

    def delete(self, entry):
        self.books.remove(entry)

    def select(self, book):
        return book if book in self.books else None
