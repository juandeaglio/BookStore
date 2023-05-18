from Source.Catalog import Catalog


class BookStore:
    def __init__(self, db):
        self.catalog = Catalog(db)

    def addToCatalog(self, books):
        self.catalog.add(books)

    def removeByTitle(self, title):
        self.catalog.removeAllByTitle(title)

    def getCatalog(self):
        return self.catalog.getAllBooks()
