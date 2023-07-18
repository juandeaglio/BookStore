from behave import given, when, then
from Source.Book import Book
from Acceptance.TestRestClient import TestRestClient


@given('An empty catalog')
def defineCatalog(context):
    context.catalog.add([])


@when('The admin adds a book to the catalog')
def addBook(context):
    book = Book("Harry Pottah", "J.K. Row", "1998")
    assert TestRestClient.createClientAsAdminAddBook(book=book) == 200


@then('There will be one more book in the catalog')
def checkForExtraBook(context):
    response = TestRestClient.createClientThatGetsCatalogAsJson()
    context.booksInCatalog = response

    assert 1 == len(context.booksInCatalog)
