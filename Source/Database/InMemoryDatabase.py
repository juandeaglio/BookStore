from Source.Interfaces.DatabaseConnection import DatabaseConnection


class InMemoryDatabase(DatabaseConnection):
    books = []

    def insertBooksIntoCatalogTable(self, booksToInsert):
        InMemoryDatabase.books += booksToInsert

    def selectAll(self):
        books = sorted(InMemoryDatabase.books,
                       key=lambda book: book.title if "The" not in book.title[0:4]
                       else book.title[4:])
        return books

    def select(self, book):
        return book if book in InMemoryDatabase.books else None

    def delete(self, entry):
        InMemoryDatabase.books.remove(entry)

    def deleteWhereTitle(self, title):
        deleted = []
        for book in InMemoryDatabase.books:
            if title in book.title:
                InMemoryDatabase.books.remove(book)
                deleted.append(book)

        return deleted

    def selectWith(self, bookDetail):
        found = []
        for book in InMemoryDatabase.books:
            if bookDetail in book.title or bookDetail in book.author:
                found.append(book)

        return sorted(found,
                      key=lambda book: book.title if "The" not in book.title[0:4]
                      else book.title[4:])

    def synchronize(self):
        return InMemoryDatabase.books

    def selectFromAllFields(self, textContent):
        found = []
        for book in InMemoryDatabase.books:
            if textContent == book.title or textContent == book.author or textContent == book.releaseYear or \
                    textContent == book.price or textContent == book.imagePath or textContent == book.description:
                found.append(book)

        return sorted(found,
                      key=lambda book: book.title if "The" not in book.title[0:4]
                      else book.title[4:])
