class BookStore:
    def __init__(self, catalog):
        self.catalog = catalog

    def addToCatalog(self, books):
        if books is None:
            pass
        else:
            self.catalog.add(books)

    def removeByTitle(self, title):
        self.catalog.removeAllByTitle(title)

    def getCatalog(self):
        return self.catalog.getAllBooks()

    def getCatalogToString(self):
        catalog = ''
        for book in self.catalog.getAllBooks():
            catalog += book.title + ", " + book.author + ", " + book.releaseYear + '\n'

        return catalog
