from behave import given, when, then
from Source.BookStore import BookStore
import pytest


@given('A catalog')
def defineCatalog(context):
    context.bookStore = BookStore()

@when('I view the catalog')
def viewCatalog(context):
    context.booksInCatalog = context.bookStore.getCatalog()

@then('The entire catalog is displayed')
def displayCatalog(context):
    assert context.booksInCatalog == context.text
