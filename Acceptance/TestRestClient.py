import requests
import urllib3

from Source.Book import Book




class TestRestClient:
    clientTimeout = 2
    userCreds = {
        'username': 'username',
        'password': 'creativepassword'
    }

    def __init__(self):
        self.session = requests.session()

    def getRequest(self, port=8091, endpoint="", host="localhost", parameters=None, timeout=clientTimeout):
        r = self.session.get(url="http://" + host + ":" + str(port) + "/" + endpoint, timeout=timeout,
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

    def sendFromSession(self, port=8091, payload=None, endpoint=None, method="post", headers=None):
        request_method = getattr(self.session, method.lower())
        if method == "post" and self.session.cookies.get('csrftoken') and headers is None:
            headers = {
                "X-CSRFToken": self.session.cookies.get("csrftoken")
            }
        statusCode = request_method(url="http://localhost:" + str(port) + "/" + endpoint, data=payload,
                                       timeout=TestRestClient.clientTimeout, headers=headers).status_code
        return statusCode

    def createClientAsAdminAddBook(self, book):
        bookDetails = book.to_json()
        self.createClientAsAdmin()
        self.withCSRF()
        return self.sendFromSession(payload=bookDetails, endpoint="catalog_service/addBook/")

    def createClientAsAdmin(self, credentials=None):
        creds = credentials or {
            'username': 'username',
            'password': 'creativepassword'
        }
        self.withCSRF()
        return self.sendFromSession(payload=creds, endpoint="catalog_service/login/")

    def createClientAddBook(self, book=None):
        self.withCSRF()
        statusCode = self.sendFromSession(payload=book.to_json(), endpoint="catalog_service/addBook/")
        return statusCode

    def searchForBook(self, title, port=8091, host="localhost", timeout=2):
        r = self.getRequest(endpoint="catalog_service/search", parameters={'title': title}, port=port, host=host,
                            timeout=timeout)
        return r

    def deleteBook(self, firstBook):
        bookDetails = firstBook.to_json()
        self.createClientAsAdmin()
        self.withCSRF()
        statusCode = self.sendFromSession(payload=bookDetails, endpoint="catalog_service/removeBook/")
        return statusCode

    def getStatic(self, port, staticfile, timeout=clientTimeout):
        try:
            r = self.getRequest(port=port, endpoint="static/" + staticfile, timeout=timeout)
            return r
        except (requests.exceptions.ConnectionError, TimeoutError) as e:
            return e

    def fetchStaticImage(self, port=8091):
        r = self.getStatic(port=port, staticfile="imgs/Emma.jpg")
        return r

    def createUser(self, username, password):
        return self.sendFromSession(payload={'username': username, 'password': password},
                                    endpoint="catalog_service/createUser/")

    def withCSRF(self):
        return self.sendFromSession(payload=None, endpoint="catalog_service/csrf/", method="get")
