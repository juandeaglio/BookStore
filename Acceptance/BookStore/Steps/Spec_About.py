from Acceptance.behave import given, when, then
from Acceptance.TestRestClient import TestRestClient


@given('An about page')
def defineCatalog(context):
    pass


@when('A user requests the about page')
def viewCatalog(context):
    response = TestRestClient().createClientForAboutPage()
    context.aboutPageResponse = response


@then('The about page is displayed')
def displayCatalog(context):
    assert "about" in context.aboutPageResponse.text.lower()
    assert context.aboutPageResponse.status_code == 200, \
        "Expected 200 OK but got " + str(context.aboutPageResponse.status_code)
