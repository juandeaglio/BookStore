from behave import given, when, then
from Acceptance.BookStore.Steps.ContextTable import convertTableToArray
from Acceptance.BookStore.Steps.HTTPContent import convertContentToArray
from Acceptance.MockWebPage.TestRestClient import TestRestClient


@given('A catalog webpage')
def defineCatalog(context):
    context.html = """
<html>
<head>
    <title> Book Catalog </title>
</head>

<body>
    <h1> Book Catalog</h1>
    <table>
        <thead>
            <tr>
                <th>Title</th>
                <th>Author</th>
                <th>Release Year</th>
            """
    context.booksFromContext = convertTableToArray(context)
    context.catalog.add(context.booksFromContext)


@when('The catalog is retrieved')
def retrieveCatalog(context):
    response = TestRestClient.createClientThatGetsCatalog()
    context.booksInCatalog = convertContentToArray(response)


@then('The entire catalog is displayed on the webpage')
def displayCatalog(context):
    books = convertTableToArray(context)
    assert arraysOfBooksAreTheSame(books, context.booksInCatalog)
