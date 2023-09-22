import re


class Book:
    def __init__(self, title='', author='', releaseYear='', imagePath='', description='', price=''):
        self.attributes = ['title', 'author', 'releaseYear', 'imagePath', 'description', 'price']
        self.title = title
        self.author = author
        self.releaseYear = releaseYear
        self.imagePath = imagePath
        self.description = description
        self.price = price

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented

        return all(getattr(self, attr) == getattr(other, attr) for attr in self.attributes)

    def to_json(self):
        return {attr: getattr(self, attr) for attr in self.attributes if hasattr(self, attr)}

    def toString(self):
        return ', '.join(str(getattr(self, attr)) for attr in self.attributes if hasattr(self, attr))
