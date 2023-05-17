from Source.Catalog import Catalog


class BookStore:
    def __init__(self):
        self.catalog = Catalog()

    def addToCatalog(self, books):
        for book in books:
            self.catalog.add(book)
        self.catalog.size += len(books)

    def removeByTitle(self, title):
        self.catalog.removeAllByTitle(title)
