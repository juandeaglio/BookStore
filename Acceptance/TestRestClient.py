import requests

from Source.Book import Book


def createClientSession(port=8091, userCreds=None, endpoint=None):
    with requests.session() as s:
        s.post(url="http://localhost:" + str(port) + "/" + endpoint, data=userCreds,
               timeout=TestRestClient.clientTimeout)

    return s


class TestRestClient:
    clientTimeout = 2
    userCreds = {
        'username': 'username',
        'password': 'creativepassword'
    }

    def __init__(self):
        self.session = requests.session()

    def getRequest(self, port=8091, endpoint="", parameters=None, timeout=clientTimeout):
        r = self.session.get(url="http://127.0.0.1:" + str(port) + "/" + endpoint, timeout=timeout,
                             params=parameters)
        return r

    def createClientThatGetsCatalog(self, port=8091):
        r = self.getRequest(port, "getCatalog")
        return r.text.splitlines()

    def createClientForAboutPage(self, port=8091, timeout=2):
        r = self.getStatic(port, staticfile="about.html", timeout=timeout)
        return r

    def createClientThatGetsCatalogAsJson(self, port=8091):
        r = self.getRequest(port, "catalog_service/fetchCatalog")
        return r.json()

    def sendPostFromSession(self, port=8091, payload=None, endpoint=None):
        statusCode = self.session.post(url="http://localhost:" + str(port) + "/" + endpoint, data=payload,
                                       timeout=TestRestClient.clientTimeout).status_code
        return statusCode

    def createClientAsAdminAddBook(self, book):
        bookDetails = book.to_json()
        self.createClientAsAdmin()
        statusCode = self.sendPostFromSession(payload=bookDetails, endpoint="catalog_service/addBook/")
        return statusCode

    def createClientAsAdmin(self):
        userCreds = {
            'username': 'username',
            'password': 'creativepassword'
        }
        return self.sendPostFromSession(payload=userCreds, endpoint="catalog_service/login/")

    def createClientAddBook(self, book=None):
        statusCode = self.sendPostFromSession(payload=book.to_json(), endpoint="catalog_service/addBook/")
        return statusCode

    def searchForBook(self, title):
        r = self.getRequest(endpoint="catalog_service/search", parameters={'title': title})
        return r

    def deleteBook(self, firstBook):
        bookDetails = firstBook.to_json()
        self.createClientAsAdmin()
        statusCode = self.sendPostFromSession(payload=bookDetails, endpoint="catalog_service/removeBook/")
        return statusCode

    def getStatic(self, port, staticfile, timeout=clientTimeout):
        r = self.getRequest(port=port, endpoint="static/"+staticfile, timeout=timeout)
        return r


