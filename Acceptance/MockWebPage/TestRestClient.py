import requests


class TestRestClient:
    clientTimeout = 0.5
    @staticmethod
    def createClientThatGetsCatalog(port=8091):
        r = requests.get(url="http://127.0.0.1:" + str(port) + "/getCatalog", timeout=TestRestClient.clientTimeout)
        return r.text.splitlines()

    @staticmethod
    def createClientForAboutPage(port=8091):
        r = requests.get(url="http://127.0.0.1:" + str(port) + "/about", timeout=TestRestClient.clientTimeout)
        return r.text

    @staticmethod
    def createClientThatGetsCatalogAsJson(port=8091):
        r = requests.get(url="http://localhost:" + str(port)
                             + "/catalog_service/fetchCatalog", timeout=TestRestClient.clientTimeout)
        return r.json()

    @staticmethod
    def asAdminAddBook(port=8091):
        with TestRestClient.loginAsAdmin()[0] as s:
            bookDetails = {
                'title': 'Some harry Potter Book',
                'author': 'J.K. ROWling',
                'releaseYear': '1899'
            }

            r = s.post(url="http://localhost:" + str(port)
                           + "/catalog_service/addBook/", data=bookDetails, timeout=TestRestClient.clientTimeout)
            print("Book addition status: " + str(r.status_code))
            return r.status_code

    @staticmethod
    def loginAsAdmin(port=8091):
        userCreds = {
            'username': 'username',
            'password': 'creativepassword'
        }
        with requests.session() as s:
            p = s.post(url="http://localhost:" + str(port)
                           + "/catalog_service/login/", data=userCreds,
                       timeout=TestRestClient.clientTimeout)
            print("Log in status: " + str(p.status_code))

            return s, p.status_code
