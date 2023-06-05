from Source.Book import Book


def convertContentToArray(body):
    books = []
    for line in body:
        fields = line.split(",")
        book = Book(title=fields[0], author=fields[1], releaseYear=fields[2])
        books.append(book)

    return books
