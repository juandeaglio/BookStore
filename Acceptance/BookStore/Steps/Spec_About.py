from behave import given, when, then
from Acceptance.BookStore.Steps.ContextTable import convertTableToArray
from Acceptance.BookStore.Steps.HTTPContent import convertContentToArray
from Source.Book import Book
from Acceptance.MockWebPage.TestRestClient import TestRestClient


@given('An about page')
def defineCatalog(context):
    pass


@when('A user requests the about page')
def viewCatalog(context):
    response = TestRestClient.createClientForAboutPage()
    context.aboutPageReceived = response


@then('The about page is displayed')
def displayCatalog(context):
    assert "about" in context.aboutPageReceived.lower()
