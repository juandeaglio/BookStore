from Source.Interfaces.DatabaseConnection import DatabaseConnection


class InMemoryDatabase(DatabaseConnection):
    def __init__(self):
        super().__init__()
        self.books = []

    def insertBooksIntoCatalogTable(self, books):
        return super().insertBooksIntoCatalogTable(books)
    
    def selectAll(self):
        return super().selectAll()

    def delete(self, entry):
        return super().delete(entry)

    def select(self, searchTerm):
        return super().select(searchTerm)

    def deleteWhereTitle(self, title):
        return super().deleteWhereTitle(title)

    def selectWith(self, bookDetail):
        return super().selectWith(bookDetail)