from Source.Interfaces.DatabaseConnection import DatabaseConnection


class InMemoryDatabase(DatabaseConnection):
    def __init__(self):
        super().__init__()

    def insertBooksIntoCatalogTable(self, books):
        return super().insertBooksIntoCatalogTable(books)
    
    def selectAll(self):
        return super().selectAll()

    def delete(self, entry):
        return super().delete(entry)

    def select(self, searchTerm, books=None):
        return super().select(searchTerm, books)

    def deleteWhereTitle(self, title):
        return super().deleteWhereTitle(title)

    def selectWith(self, bookDetail):
        return super().selectWith(bookDetail)