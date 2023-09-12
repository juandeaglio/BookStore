import unittest
from Source.Response import Response


class ResponseTest(unittest.TestCase):
    def test_sameResponsesAreEqual(self):
        response1 = Response()
        response2 = Response()
        assert response1 == response2

    def test_differentResponsesNotEqual(self):
        response1 = Response(start="HTTP/2.1 404 NOT FOUND", body="Hello1234", parameters={"cors": "*", "content-type": "json"})
        response2 = Response(start="HTTP/1.1 200 OK", body="Hello123", parameters={"cors": "none", "content-type": "plaintext"})

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

    def test_rawHasSameParameters(self):
        regularResponse = \
            Response(parameters={"Access-Control-Allow-Origin": "*", "Content-Type": "text/plain"}, body="hello")
        assert regularResponse.headers == self.bytesResponse.headers

    def test_rawHasSameBody(self):
        regularResponse = Response(body="hello")

        assert regularResponse.body == self.bytesResponse.body
        assert regularResponse.headers['Content-Length'] == self.bytesResponse.headers['Content-Length']
