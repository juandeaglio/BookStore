from behave import given, when, then
from Source.Book import Book
from Acceptance.TestRestClient import TestRestClient


@given('An empty catalog')
def defineCatalog(context):
    context.catalog.add([])


@when('The admin adds a book to the catalog')
def addBook(context):
    book = Book(title="Harry Pottah", author="J.K. Row", releaseYear="1998", price="$10.00",
                imagePath="static/imgs/Harry Pottah.jpg", description="Random description")
    assert TestRestClient().createClientAsAdminAddBook(book=book) == 200


@then('There will be one more book in the catalog')
def checkForExtraBook(context):
    response = TestRestClient().createClientThatGetsCatalogAsJson()
    context.booksInCatalog = response
    assert 1 == len(context.booksInCatalog)
    response = TestRestClient().getBooksWithEmptyFields()
    context.booksInCatalog = response
    print("Empty books found: " + str(context.booksInCatalog))
    assert 0 == len(context.booksInCatalog)


@when('An unauthorized user try to add a book to the catalog')
def addBook(context):
    book = Book("Harry Pottah", "J.K. Row", "1998")
    assert TestRestClient().createClientAddBook(book=book) != 200


@then('The user will be denied and the catalog is still empty')
def checkForExtraBook(context):
    response = TestRestClient().createClientThatGetsCatalogAsJson()
    context.booksInCatalog = response
    assert 0 == len(context.booksInCatalog)
