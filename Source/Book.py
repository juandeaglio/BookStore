import re


class Book:
    def __init__(self, title="", author="", releaseYear=""):
        self.title = title
        self.author = author
        self.releaseYear = releaseYear

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented

        return self.title == other.title and self.author == other.author and self.releaseYear == other.releaseYear

    def toString(self):
        return self.title + ", " + self.author + ", " + self.releaseYear
