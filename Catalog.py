class Catalog:
    def __init__(self):
        self.size = 0
        self.bookRepository = []

    def add(self, book):
        self.bookRepository.append(book)

    def removeAllByTitle(self, title):
        for book in self.bookRepository:
            if title in book['Title']:
                self.bookRepository.remove(book)
                self.size -= 1
