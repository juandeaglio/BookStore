# Short description
A pretty basic and simple book store.
There is a catalog which serves suggestions based on category.
An online store with a shopping cart.
![Early website design](https://gitfront.io/r/user-9745374/D8ZrCkf4bx8U/BookStore/raw/EarlyWebsiteDesign.png)

Wrote a simple webserver that provides the current inventory of books to clients.
Used Javascript + HTML + CSS for the webpage.

Store page and shopping cart are not implemented yet.

### To run behave tests:
Run in base project directory
****
behave .\Acceptance\BookStore\ --no-capture --no-capture-stderr #this just spits everything out to terminal)\
behave -f allure_behave.formatter:AllureFormatter -o allure_reports/ .\Acceptance\BookStore\ #prints in terminal but generates a report, viewable by below allure cmd
### To view BDD test results (opens your web browser to view results):
Run in base project directory
****
allure serve allure_reports