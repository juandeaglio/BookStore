from Source.Interfaces.DatabaseConnection import DatabaseConnection


class InMemoryDatabase(DatabaseConnection):
    def __init__(self):
        self.books = []

    def insertBooksIntoCatalogTable(self, booksToInsert):
        self.books += booksToInsert

    def selectAll(self):
        books = sorted(self.books,
                       key=lambda book: book.title if "The" not in book.title[0:4]
                       else book.title[4:])
        return books

    def select(self, book):
        return book if book in self.books else None

    def delete(self, entry):
        self.books.remove(entry)

    def deleteWhereTitle(self, title):
        deleted = []
        for book in self.books:
            if title in book.title:
                self.books.remove(book)
                deleted.append(book)

        return deleted

    def selectWith(self, bookDetail):
        found = []
        for book in self.books:
            if bookDetail in book.title or bookDetail in book.author:
                found.append(book)

        return sorted(found,
                      key=lambda book: book.title if "The" not in book.title[0:4]
                      else book.title[4:])

    def selectWithStrict(self, bookDetail):
        found = []
        for book in self.books:
            if bookDetail == book.title or bookDetail == book.author:
                found.append(book)

        return sorted(found,
                      key=lambda book: book.title if "The" not in book.title[0:4]
                      else book.title[4:])
    def synchronize(self):
        return self.books

    def selectFromAllFields(self, textContent):
        found = []
        for book in self.books:
            if textContent == book.title or textContent == book.author or textContent == book.releaseYear or \
                    textContent == book.price or textContent == book.imagePath or textContent == book.description:
                found.append(book)

        return sorted(found,
                      key=lambda book: book.title if "The" not in book.title[0:4]
                      else book.title[4:])
