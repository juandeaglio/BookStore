import re

from Source.Book import Book


def makeBookFromSQL(columns, row):
    book = Book()
    for i in range(len(columns)):
        setattr(book, columns[i][0], row[i])
    return book


def get_books_changed(sqlData):
    rows, columns = sqlData
    books = []
    for row in rows:
        book = makeBookFromSQL(columns, row)

        cleanDoubleQuotesFromTitle(book)
        books.append(book)
    return books


def replace_single_quote_with_double(entry):
    # SQL requirement for single quote character ' in field.
    newEntry = Book()
    if isinstance(entry, str):
        newEntry = re.sub("'", "''", entry)

    else:
        for attribute in entry.attributes:
            # check if the entry.attribute has a single quote
            if "'" in getattr(entry, attribute):
                setattr(newEntry, attribute, re.sub("'", "''", getattr(entry, attribute)))
            else:
                setattr(newEntry, attribute, getattr(entry, attribute))

    return newEntry


def cleanDoubleQuotesFromTitle(book):
    # SQL requirement for quotes in field (must be double-quoted)
    removeDuplicateQuotes(book)


def removeDuplicateQuotes(book):
    for attribute in book.attributes:
        setattr(book, attribute, re.sub("''", "'", getattr(book, attribute)))


def titleHasDoubleQuote(book):
    return "\'\'" in book.title
