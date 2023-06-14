import unittest
from Source.Response import Response
from Source.Response import StatusCode


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

    def test_rawHasSameVersion(self):
        bytesResponse = Response(raw=bytes("HTTP/1.1 200 OK\n" + "Access-Control-Allow-Origin: *\n"
                                           + "Content-Type: text/plain\n" + "Content-Length: " + str(len("hello")) +
                                           "\n" + "\n" + "hello", "UTF-8"))
        regularResponse = Response(start="HTTP/1.1 200 OK")

        assert regularResponse.statusCode == bytesResponse.statusCode
        assert regularResponse.version == bytesResponse.version

    def test_rawHasSameRequestParameters(self):
        bytesResponse = Response(raw=bytes("HTTP/1.1 200 OK\n" + "Access-Control-Allow-Origin: *\n"
                                           + "Content-Type: text/plain\n" + "Content-Length: " + str(len("hello")) +
                                           "\n" + "\n" + "hello", "UTF-8"))
        regularResponse = Response(requestParams={"Access-Control-Allow-Origin": "*"})

        assert regularResponse.requestHeaders == bytesResponse.requestHeaders

    def test_rawHasSameResponseParameters(self):
        bytesResponse = Response(raw=bytes("HTTP/1.1 200 OK\n" + "Access-Control-Allow-Origin: *\n"
                                           + "Content-Type: text/plain\n" + "Content-Length: " + str(len("hello")) +
                                           "\n" + "\n" + "hello", "UTF-8"))
        regularResponse = Response(responseParams={"Content-Type": "text/plain"}, body="Hello")

        assert regularResponse.responseHeaders == bytesResponse.responseHeaders

    def test_rawHasSameBody(self):
        bytesResponse = Response(raw=bytes("HTTP/1.1 200 OK\n" + "Access-Control-Allow-Origin: *\n"
                                           + "Content-Type: text/plain\n" + "Content-Length: " + str(len("hello")) +
                                           "\n" + "\n" + "hello", "UTF-8"))
        regularResponse = Response(body="hello")

        assert regularResponse.body == bytesResponse.body
        assert regularResponse.responseHeaders['Content-Length'] == bytesResponse.responseHeaders['Content-Length']


