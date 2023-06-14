import unittest
from Source.Response import Response
from Source.Response import StatusCode


class ResponseTest(unittest.TestCase):
    def test_sameResponsesAreEqual(self):
        response1 = Response()
        response2 = Response()
        assert response1 == response2

    def test_responseWithVersion(self):
        response = Response(start="HTTP/1.1 200 OK")
        expectedVersion = "HTTP/1.1"

        assert response.version == expectedVersion
        

    def test_responseWithStatusCode(self):
        response = Response(start="HTTP/1.1 200 OK")
        expectedStatusCode = StatusCode()
        expectedStatusCode.message = "200 OK"
        expectedStatusCode.number = 200

        assert response.statusCode == expectedStatusCode

    def test_responseWithRequestParameters(self):
        response = Response(requestParams={"cors": "*"})
        assert response.requestHeaders['cors'] == "*"

    def test_responseWithResponseParameters(self):
        response = Response(responseParams={"cors": "*"})
        assert response.responseHeaders['cors'] == "*"

    def test_differentResponsesNotEqual(self):
        response1 = Response(start="HTTP/2.1 404 NOT FOUND", body="Hello1234", requestParams={"cors": "*"},
                             responseParams={"content-type": "json"})
        response2 = Response(start="HTTP/1.1 200 OK", body="Hello123", requestParams={"cors": "none"},
                    responseParams={"content-type": "plaintext"})

        assert response1 != response2