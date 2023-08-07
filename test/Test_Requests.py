import unittest

from Source.Request import Request


class RequestsTestCase(unittest.TestCase):
    def test_parseGetCatalogPathInCatalogRequest(self):
        expectedRequest = "GET /getCatalog HTTP/1.1\r\n\r\n"
        assert "getCatalog" == Request(raw=expectedRequest).path

    def test_parseAboutPathInCatalogRequest(self):
        expectedRequest = "GET /about HTTP/1.1\r\n\r\n"
        assert "about" == Request(raw=expectedRequest).path


if __name__ == '__main__':
    unittest.main()
