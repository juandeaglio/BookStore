from Source.Interfaces.DatabaseConnection import DatabaseConnection


class InMemoryDatabase(DatabaseConnection):
    def insertBooksIntoCatalogTable(self, books, booksToInsert):
        books += booksToInsert

    def selectAll(self, books):
        books = sorted(books,
                       key=lambda book: book.title if "The" not in book.title[0:4]
                       else book.title[4:])
        return books

    def select(self, book, books):
        return book if book in books else None

    def delete(self, entry, books):
        books.remove(entry)

    def deleteWhereTitle(self, title, books):
        deleted = []
        for book in books:
            if title in book.title:
                books.remove(book)
                deleted.append(book)

        return deleted

    def selectWith(self, bookDetail, books):
        found = []
        for book in books:
            if bookDetail in book.title or bookDetail in book.author:
                found.append(book)

        return sorted(found,
                      key=lambda book: book.title if "The" not in book.title[0:4]
                      else book.title[4:])

    def synchronize(self, books):
        return books

    def selectFromAllFields(self, textContent, books):
        found = []
        for book in books:
            if textContent == book.title or textContent == book.author or textContent == book.releaseYear or \
                    textContent == book.price or textContent == book.imagePath or textContent == book.description:
                found.append(book)

        return sorted(found,
                      key=lambda book: book.title if "The" not in book.title[0:4]
                      else book.title[4:])
