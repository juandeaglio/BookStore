import io

from Source.StatusCode import StatusCode


class Response:
    def __init__(self, body=None, raw=None, start=None, requestParams=None, responseParams=None):
        self.responseHeaders = {}
        self.requestHeaders = {}
        self.setRequestHeader(requestParams)
        self.setResponseHeader(responseParams)
        self.version = None
        self.statusCode = StatusCode()
        self.body = ""

        self.parseRaw(raw)
        if body is not None:
            self.body = body
        self.responseHeaders['Content-Length'] = str(len(self.body))
        self.setVersion(start)
        self.setStatusCode(start)

    def setRequestHeader(self, params):
        self.requestHeaders = {}
        if isinstance(params, dict):
            self.requestHeaders = params

    def setResponseHeader(self, params):
        self.responseHeaders = {}
        if isinstance(params, dict):
            self.responseHeaders = params

    def parseWithoutStringIO(self, httpData):
        startLine = httpData.strip()
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
        return stringIOResponse.readline()

    def stringsToDictionary(self, byteData):
        requestHeadersLine = byteData.readline().strip()
        while "Content" not in requestHeadersLine:
            requestHeadersLine = self.parseLineIntoHeader(byteData, requestHeadersLine, self.requestHeaders)

        return requestHeadersLine

    def parseBody(self, data):
        self.body = data
        assert len(data) == int(self.responseHeaders["Content-Length"])

    def parseContentLength(self, bodyHeadersLine):
        self.responseHeaders[bodyHeadersLine.split(":")[0]] = bodyHeadersLine.split(":")[1].strip()

    def parseResponseHeaders(self, bodyHeadersLine, byteData):
        while "Content-Length" not in bodyHeadersLine:
            bodyHeadersLine = self.parseLineIntoHeader(byteData, bodyHeadersLine, self.responseHeaders)

        return bodyHeadersLine


    @staticmethod
    def parseLineIntoHeader(byteData, requestHeadersLine, headers):
        header = requestHeadersLine.split(":")
        headers[header[0].strip()] = header[1].strip()
        requestHeadersLine = byteData.readline().strip()
        return requestHeadersLine

    def setVersion(self, text):
        if isinstance(text, str):
            self.version = text.split(" ")[0]

    def setStatusCode(self, text):
        if isinstance(text, str):
            self.statusCode = StatusCode(startLine=text.strip())

    def __eq__(self, other):
        return self.body == other.body and self.responseHeaders == other.responseHeaders and \
               self.requestHeaders == other.requestHeaders and self.version == other.version and \
               self.statusCode == other.statusCode

