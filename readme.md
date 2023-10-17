I'm happy to demo and explain my code. I'm open for changes in the front or backend.

This is the live website on Azure:
http://bookhaven.eastus.cloudapp.azure.com/

# Short description
An API for an online store with a shopping cart.
![Early website design](https://github.com/juandeaglio/BookStore/blob/master/EarlyWebsiteDesign.png)

Built with Django in the backend and React in the frontend. 

My GitHub action currently has the latest on how to properly set up and run the website along with how to run the tests.

### To run behave tests:
python integrationTests.py
****
Alternatively, run in base project directory
****
behave .\Acceptance\BookStore\ --no-capture --no-capture-stderr 

prints in terminal but generates a report, viewable by below allure cmd
behave -f allure_behave.formatter:AllureFormatter -o allure_reports/ .\Acceptance\BookStore\ 

### To view BDD test results use behave in the terminal or use allure (opens your web browser to view results):
Run in base project directory
****
allure serve allure_reports

I've had a bumpy road integrating Django with React, especially with some specific features like CORS, CSRF, and dynamically configuring nginx as needed. I'm including my road through development on anthonyvolkovportfolio.com
