import unittest
from Source.Response import Response
from Source.StatusCode import StatusCode


class ResponseTest(unittest.TestCase):
    def test_sameResponsesAreEqual(self):
        response1 = Response()
        response2 = Response()
        assert response1 == response2

    def test_differentResponsesNotEqual(self):
        response1 = Response(start="HTTP/2.1 404 NOT FOUND", body="Hello1234", requestParams={"cors": "*"},
                             responseParams={"content-type": "json"})
        response2 = Response(start="HTTP/1.1 200 OK", body="Hello123", requestParams={"cors": "none"},
                             responseParams={"content-type": "plaintext"})

        assert response1 != response2


class RawResponseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.bytesResponse = Response(raw=bytes("HTTP/1.1 200 OK\n" + "Access-Control-Allow-Origin: *\n"
                                                + "Content-Type: text/plain\n" + "Content-Length: "
                                                + str(len("hello")) + "\n" + "\n" + "hello", "UTF-8"))
    def test_rawHasSameVersion(self):
        regularResponse = Response(start="HTTP/1.1 200 OK")

        assert regularResponse.statusCode == self.bytesResponse.statusCode
        assert regularResponse.version == self.bytesResponse.version

    def test_rawHasSameRequestParameters(self):
        regularResponse = Response(requestParams={"Access-Control-Allow-Origin": "*"})
        assert regularResponse.requestHeaders == self.bytesResponse.requestHeaders

    def test_rawHasSameResponseParameters(self):
        regularResponse = Response(responseParams={"Content-Type": "text/plain"}, body="Hello")
        assert regularResponse.responseHeaders == self.bytesResponse.responseHeaders

    def test_rawHasSameBody(self):
        regularResponse = Response(body="hello")

        assert regularResponse.body == self.bytesResponse.body
        assert regularResponse.responseHeaders['Content-Length'] == self.bytesResponse.responseHeaders['Content-Length']
