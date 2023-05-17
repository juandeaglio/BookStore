from Source.DatabaseConnection import DatabaseConnection


class InMemoryDatabase(DatabaseConnection):
    def __init__(self):
        self.books = []

    def insert(self, books):
        oldLen = len(self.books)
        for book in books:
            if book not in self.books:
                self.books.append(book)

        if len(self.books) != oldLen:
            return self.books
        else:
            return None

    def selectAll(self):
        return self.books

    def delete(self, entry):
        self.books.remove(entry)

    def select(self, book):
        return book if book in self.books else None
