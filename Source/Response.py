import io

from Source.StatusCode import StatusCode


class Response:
    def __init__(self, body=None, raw=None, start=None, parameters=None):
        self.headers = {}
        self.setHeaders(parameters)
        self.version = None
        self.statusCode = StatusCode()
        self.body = ""

        self.parseRaw(raw)
        if body is not None:
            self.body = body
        self.headers['Content-Length'] = str(len(self.body))
        self.setVersion(start)
        self.setStatusCode(start)

    def setHeaders(self, params):
        self.headers = {}
        if isinstance(params, dict):
            self.headers = params

    def parseWithoutStringIO(self, httpData):
        startLine = httpData[0].strip()
        self.setVersion(startLine)
        self.setStatusCode(startLine)
    def parseRaw(self, rawBytes):
        if isinstance(rawBytes, bytes):
            stringIOResponse = io.StringIO(rawBytes.decode("UTF-8"))
            httpData = self.convertToStringArray(io.StringIO(rawBytes.decode("UTF-8")))
            self.parseWithoutStringIO(httpData)
            stringIOResponse.readline()
            bodyHeadersLine = self.stringsToDictionary(stringIOResponse)
            body = self.parseResponseHeaders(bodyHeadersLine, stringIOResponse)
            self.parseContentLength(body)
            assert stringIOResponse.readline() == '\n'
            self.parseBody(stringIOResponse.read())

    def convertToStringArray(self, stringIOResponse):
        return stringIOResponse.readlines()

    def stringsToDictionary(self, byteData):
        headersLine = byteData.readline().strip()
        while "Content" not in headersLine:
            headersLine = self.parseLineIntoHeader(byteData, headersLine, self.headers)

        return headersLine

    def parseBody(self, data):
        self.body = data
        assert len(data) == int(self.headers["Content-Length"])

    def parseContentLength(self, bodyHeadersLine):
        self.headers[bodyHeadersLine.split(":")[0]] = bodyHeadersLine.split(":")[1].strip()

    def parseResponseHeaders(self, bodyHeadersLine, byteData):
        while "Content-Length" not in bodyHeadersLine:
            bodyHeadersLine = self.parseLineIntoHeader(byteData, bodyHeadersLine, self.headers)

        return bodyHeadersLine


    @staticmethod
    def parseLineIntoHeader(byteData, headersLine, headers):
        header = headersLine.split(":")
        headers[header[0].strip()] = header[1].strip()
        headersLine = byteData.readline().strip()
        return headersLine

    def setVersion(self, text):
        if isinstance(text, str):
            self.version = text.split(" ")[0]

    def setStatusCode(self, text):
        if isinstance(text, str):
            self.statusCode = StatusCode(startLine=text.strip())

    def __eq__(self, other):
        return self.body == other.body and self.headers == other.headers and \
               self.headers == other.headers and self.version == other.version and \
               self.statusCode == other.statusCode

