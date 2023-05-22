from behave import given, when, then, fixture, use_fixture
from Source.BookStore import BookStore
from Source.Catalog import Catalog
from Source.SqlDatabase import SqlDatabase


@given('A catalog')
def defineCatalog(context):
    context.bookStore = BookStore(Catalog(SqlDatabase()))
    books = convertTableToArray(context)
    context.bookStore.addToCatalog(books)
    print(context.bookStore.getCatalog())


@when('I view the catalog')
def viewCatalog(context):
    context.booksInCatalog = context.bookStore.getCatalog()


@then('The entire catalog is displayed')
def displayCatalog(context):
    books = convertTableToArray(context)
    for element, otherElement in zip(books, context.bookStore.getCatalog()):
        assert theSame(element, otherElement)


def theSame(book, otherBook):
    return book == otherBook


def convertTableToArray(context):
    books = []
    for book in context.table:
        books.append({'Title': book[0], 'Author': book[1], 'Release year': book[2]})
    return books
