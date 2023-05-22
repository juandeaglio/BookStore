from Source.CatalogInterface import CatalogInterface


class BookStore:
    def __init__(self, catalog):
        self.catalog = catalog

    def addToCatalog(self, books):
        self.catalog.add(books)

    def removeByTitle(self, title):
        self.catalog.removeAllByTitle(title)

    def getCatalog(self):
        return self.catalog.getAllBooks()
