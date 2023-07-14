# Short description
A pretty basic and simple book store.
There is a catalog which serves suggestions based on category.
An online store with a shopping cart.
![Early website design](https://gitfront.io/r/user-9745374/D8ZrCkf4bx8U/BookStore/raw/EarlyWebsiteDesign.png)

Wrote a simple webserver that provides the current inventory of books to clients.
Used Javascript + HTML + CSS for the webpage.

Store page and shopping cart are not implemented yet.

### To run behave tests:
python integrationTests.py
****
Alternatively, run in base project directory
****
behave .\Acceptance\BookStore\ --no-capture --no-capture-stderr #this just spits everything out to terminal)
behave .\Acceptance\BookStore\ --no-capture --no-capture-stderr -n "Name of Test Scenario as seen in any .feature"
behave .\Acceptance\BookStore\ --no-capture --no-capture-stderr -n "View a persistent catalog"
behave -f allure_behave.formatter:AllureFormatter -o allure_reports/ .\Acceptance\BookStore\ #prints in terminal but generates a report, viewable by below allure cmd
### To view BDD test results (opens your web browser to view results):
Run in base project directory
****
allure serve allure_reports

#### How I use Behave:
There's a lot of detailed stuff in environments.py that have details on how tests must start, particularly since
there is some coupling with the tests and the Django webserver. None of the tests have any Django code in them, so the
test cases themselves don't directly depend on anything I write in Django, all that matters is that the API provides the
expected response. Ideally, environments.py will at most start the Django server in the background and that's all.
Whereas the tests themselves, it's mostly a pretty quickly-written HTTP client written with the 'requests' library.