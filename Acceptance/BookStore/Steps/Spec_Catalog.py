from behave import given, when, then
from Source.Book import Book
from Acceptance.TestRestClient import TestRestClient


def convertContentToArray(body):
    books = []
    for line in body:
        fields = line.split(",")
        book = Book(title=fields[0], author=fields[1], releaseYear=fields[2])
        books.append(book)

    return books


@given('A catalog')
def defineCatalog(context):
    context.booksFromContext = convertTableToArray(context)
    context.catalog.add(context.booksFromContext)


@when('A user views the catalog')
def viewCatalog(context):
    response = TestRestClient.createClientThatGetsCatalog()
    context.booksInCatalog = convertContentToArray(response)


def arraysOfBooksAreTheSame(books, booksInCatalog):
    for book, otherBook in zip(books, booksInCatalog):
        if book != otherBook:
            print("1: " + book.title + " " + book.author + " " + book.releaseYear)
            print("2: " + otherBook.title + " " + otherBook.author + " " + otherBook.releaseYear)
            return False
    return True


@then('The entire catalog is displayed')
def displayCatalog(context):
    print("vs. ")
    books = convertTableToArray(context)
    assert arraysOfBooksAreTheSame(books, context.booksInCatalog)


# TODO re-do below tests to mimic above one.
@given('An empty catalog')
def defineCatalog(context):
    context.catalog.add([])


@when('The admin adds a book to the catalog')
def addBook(context):
    book = Book(title="Some Harry Potter Book, I think.", author="Just Kidding Rowling", releaseYear="1998")
    context.catalog.add([book])


@then('There will be one more book in the catalog')
def checkForExtraBook(context):
    response = TestRestClient.createClientThatGetsCatalog()
    context.booksInCatalog = convertContentToArray(response)

    assert 1 == len(context.booksInCatalog)


@when('The admin add a duplicate book to the catalog')
def addBook(context):
    alreadyAddedBook = context.booksFromContext[0]
    context.catalog.add([alreadyAddedBook])


@then('There will be no changes to the catalog')
def checkForExtraBook(context):
    response = TestRestClient.createClientThatGetsCatalog()
    context.booksInCatalog = convertContentToArray(response)
    expectedBooks = convertTableToArray(context)

    assert len(expectedBooks) == len(context.booksInCatalog)


def convertTableToArray(context):
    books = []
    for book in context.table:
        new = Book(title=book[0], author=book[1], releaseYear=book[2])
        books.append(new)

    return books
