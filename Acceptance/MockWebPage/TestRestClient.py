import requests

from Source.Book import Book


class TestRestClient:
    clientTimeout = 1

    @staticmethod
    def getRequest(port, endpoint):
        r = requests.get(url="http://127.0.0.1:" + str(port) + "/" + endpoint, timeout=TestRestClient.clientTimeout)
        return r

    @staticmethod
    def createClientThatGetsCatalog(port=8091):
        r = TestRestClient.getRequest(port, "getCatalog")
        return r.text.splitlines()

    @staticmethod
    def createClientForAboutPage(port=8091):
        r = TestRestClient.getRequest(port, "about")
        return r.text

    @staticmethod
    def createClientThatGetsCatalogAsJson(port=8091):
        r = TestRestClient.getRequest(port, "catalog_service/fetchCatalog")
        return r.json()

    @staticmethod
    def createClientSession(port, userCreds, endpoint):
        with requests.session() as s:
            p = s.post(url="http://localhost:" + str(port) + "/" + endpoint, data=userCreds,
                       timeout=TestRestClient.clientTimeout)
            print("Log in status: " + str(p.status_code))
        return s

    @staticmethod
    def sendPostFromSession(port, userCreds, endpoint, existingSession=requests.session()):
        statusCode = existingSession.post(url="http://localhost:" + str(port) + "/" + endpoint, data=userCreds,
                                          timeout=TestRestClient.clientTimeout).status_code
        print("Log in status: " + str(statusCode))
        return statusCode

    @staticmethod
    def createClientAsAdminAddBook(port=8091, book=None):
        userCreds = {
            'username': 'username',
            'password': 'creativepassword'
        }
        with TestRestClient.createClientSession(port, userCreds, "catalog_service/login/") as loggedInSession:
            bookDetails = {
                'title': book.title,
                'author': book.author,
                'releaseYear': book.releaseYear
            }
            statusCode = TestRestClient.sendPostFromSession(port, bookDetails,
                                                            "catalog_service/addBook/", loggedInSession)
            print("Book addition status: " + str(statusCode))
        return statusCode

    @staticmethod
    def createClientAsAdmin(port=8091):
        userCreds = {
            'username': 'username',
            'password': 'creativepassword'
        }
        return TestRestClient.sendPostFromSession(port, userCreds, "catalog_service/login/")
