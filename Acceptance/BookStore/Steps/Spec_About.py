from behave import given, when, then
from Acceptance.TestRestClient import TestRestClient


@given('An about page')
def defineCatalog(context):
    pass


@when('A user requests the about page')
def viewCatalog(context):
    response = TestRestClient().createClientForAboutPage()
    context.aboutPageReceived = response


@then('The about page is displayed')
def displayCatalog(context):
    assert "about" in context.aboutPageReceived.lower()
