import io


class StatusCode:
    def __init__(self):
        self.number = -1
        self.message = ""

    def __eq__(self, other):
        return self.number == other.number and self.message == other.message


class Response:
    def __init__(self, body=None, raw=None, start=None, requestParams={}, responseParams={}):
        self.requestHeaders = requestParams
        self.responseHeaders = responseParams
        self.version = None
        self.statusCode = StatusCode()
        self.contentLength = 0
        self.body = ""
        if raw is not None:
            self.parseRaw(raw)
        if body is not None:
            self.body = body
            self.contentLength = len(self.body)
        if start is not None:
            self.parseStartLine(start)

    def parseRaw(self, rawBytes):
        byteData = io.StringIO(rawBytes.decode("UTF-8"))
        self.parseStartLine(byteData.readline())
        bodyHeadersLine = self.parseRequestHeaders(byteData)
        body = self.parseResponseHeaders(bodyHeadersLine, byteData)
        self.parseContentLength(body)
        assert byteData.readline() == '\n'
        self.parseBody(byteData.read())

    def parseBody(self, data):
        self.body = data
        length = len(data)
        assert length == self.responseHeaders["Content-Length"]

    def parseContentLength(self, bodyHeadersLine):
        self.responseHeaders[bodyHeadersLine.split(":")[0]] = int(bodyHeadersLine.split(":")[1])

    def parseResponseHeaders(self, bodyHeadersLine, byteData):
        while "Content-Length" not in bodyHeadersLine:
            bodyHeadersLine = self.parseLineIntoHeader(byteData, bodyHeadersLine, self.responseHeaders)

        return bodyHeadersLine

    def parseRequestHeaders(self, byteData):
        requestHeadersLine = byteData.readline().strip()
        while "Content" not in requestHeadersLine:
            requestHeadersLine = self.parseLineIntoHeader(byteData, requestHeadersLine, self.requestHeaders)

        return requestHeadersLine

    @staticmethod
    def parseLineIntoHeader(byteData, requestHeadersLine, headers):
        header = requestHeadersLine.split(":")
        headers[header[0].strip()] = header[1].strip()
        requestHeadersLine = byteData.readline().strip()
        return requestHeadersLine

    def parseStartLine(self, text):
        startLine = text.strip()
        self.version = startLine.split(" ")[0]
        self.statusCode.number = int(startLine.split(" ")[1])
        self.statusCode.message = startLine.split(" ")[1] + " " + startLine.split(" ")[2]

    def __eq__(self, other):
        return self.body == other.body and self.responseHeaders == other.responseHeaders and \
               self.requestHeaders == other.requestHeaders and self.version == other.version and \
               self.statusCode == other.statusCode and self.contentLength == other.contentLength
