from Source.Book import Book


def convertTableToArray(context):
    books = []
    for book in context.table:
        new = Book(title=book[0], author=book[1], releaseYear=book[2])
        books.append(new)

    return books
