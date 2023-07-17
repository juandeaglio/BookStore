import time

from behave import given, when, then
from Acceptance.BookStore.Steps.ContextTable import convertTableToArray
from Acceptance.BookStore.Steps.HTTPContent import convertContentToArray
from Source.Book import Book
from Acceptance.MockWebPage.TestRestClient import TestRestClient
from Source.Catalog.InMemoryCatalog import InMemoryCatalog


def createExpectedJson(books):
    fakeCatalog = InMemoryCatalog()
    fakeCatalog.add(books)
    books = fakeCatalog.getAllBooksJson()
    return books


@given('A catalog')
def defineCatalog(context):
    context.booksFromContext = convertTableToArray(context)
    context.catalog.add(context.booksFromContext)


@when('A user views the catalog')
def viewCatalog(context):
    response = TestRestClient.createClientThatGetsCatalogAsJson()
    context.jsonCatalog = response


@then('The entire catalog is displayed')
def displayCatalog(context):
    books = convertTableToArray(context)
    books = createExpectedJson(books)
    jsonBooks = context.jsonCatalog
    assert jsonBooks == books


@given('A user has admin permissions')
def createAdminUser(context):
    #add user as admin
    pass

@when('A user logs in as an admin')
def loginAsAdmin(context):
    context.session = TestRestClient.loginAsAdmin()


@then('The user can access admin pages')
def loggedInAsAdmin(context):
    success = context.session[1]
    assert 200 == success


@given('An empty catalog')
def defineCatalog(context):
    context.catalog.add([])


@when('The admin adds a book to the catalog')
def addBook(context):
    assert TestRestClient.asAdminAddBook() == 200


@then('There will be one more book in the catalog')
def checkForExtraBook(context):
    response = TestRestClient.createClientThatGetsCatalogAsJson()
    context.booksInCatalog = response

    assert 1 == len(context.booksInCatalog)


@when('The admin add a duplicate book to the catalog')
def addBook(context):
    alreadyAddedBook = context.booksFromContext[0]
    context.catalog.add([alreadyAddedBook])


@then('There will be no changes to the catalog')
def checkForExtraBook(context):
    response = TestRestClient.createClientThatGetsCatalogAsJson()
    context.booksInCatalog = response
    books = convertTableToArray(context)
    fakeCatalog = InMemoryCatalog()
    fakeCatalog.add(books)
    books = fakeCatalog.getAllBooksJson()

    assert len(books) == len(context.booksInCatalog)


