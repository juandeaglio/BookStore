![alt text](http://url/to/img.png)

# Commands you can run in base project directory:
## To run behave tests:
behave .\Acceptance\BookStore\ --no-capture --no-capture-stderr #this just spits everything out to terminal)\
behave -f allure_behave.formatter:AllureFormatter -o allure_reports/ .\Acceptance\BookStore\ #prints in terminal but generates a report, viewable by below allure cmd
## To view BDD test results (opens your web browser to view results):
allure serve allure_reports