from Source.Interfaces.DatabaseConnection import DatabaseConnection


class InMemoryDatabase(DatabaseConnection):
    def __init__(self):
        self.books = []

    def insertBooksIntoCatalogTable(self, books):
        oldLen = len(self.books)
        for book in books:
            self.books.append(book)

        if len(self.books) != oldLen:
            return self.books
        else:
            return None

    def selectAll(self):
        self.books = sorted(self.books,
                            key=lambda book: book.title if "The" not in book.title[0:4]
                            else book.title[4:])
        return self.books

    def delete(self, entry):
        self.books.remove(entry)

    def select(self, book):
        return book if book in self.books else None

    def selectWhereTitle(self, title):
        found = []
        for book in self.books:
            if title in book.title:
                found.append(book)

        return found

    def deleteWhereTitle(self, title):
        deleted = 0
        for book in self.books:
            if title in book.title:
                self.books.remove(book)
                deleted += 1

        return deleted