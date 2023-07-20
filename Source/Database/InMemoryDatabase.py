from Source.Interfaces.DatabaseConnection import DatabaseConnection


class InMemoryDatabase(DatabaseConnection):
    def __init__(self):
        super().__init__()

    def insertBooksIntoCatalogTable(self, books, booksToInsert):
        return super().insertBooksIntoCatalogTable(books, booksToInsert)
    
    def selectAll(self, books):
        return super().selectAll(books)

    def delete(self, entry, books):
        return super().delete(entry, books)

    def select(self, searchTerm, books=None):
        return super().select(searchTerm, books)

    def deleteWhereTitle(self, title, books):
        return super().deleteWhereTitle(title, books)

    def selectWith(self, bookDetail, books):
        return super().selectWith(bookDetail, books)
