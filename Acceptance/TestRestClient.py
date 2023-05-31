import requests


class TestRestClient:
    @staticmethod
    def createClientThatGetsCatalog(port=8091):
        r = requests.get(url="http://127.0.0.1:" + str(port) + "/getCatalog", timeout=0.1)
        return r.text.splitlines()
