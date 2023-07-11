import requests


class TestRestClient:
    @staticmethod
    def createClientThatGetsCatalog(port=8091):
        r = requests.get(url="http://127.0.0.1:" + str(port) + "/getCatalog", timeout=0.01)
        return r.text.splitlines()

    @staticmethod
    def createClientForAboutPage(port=8091):
        r = requests.get(url="http://127.0.0.1:" + str(port) + "/about", timeout=0.01)
        return r.text

    @staticmethod
    def createClientThatGetsCatalogAsJson(port=8091):
        r = requests.get(url="http://localhost:" + str(port) + "/catalog_service/fetchCatalog", timeout=0.01)
        return r.json()
