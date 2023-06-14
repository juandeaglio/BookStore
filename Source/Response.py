import io


class StatusCode:
    def __init__(self):
        self.number = -1
        self.message = ""

    def __eq__(self, other):
        return self.number == other.number and self.message == other.message


class Response:
    def __init__(self, body=None, raw=None, start=None, requestParams=None, responseParams=None):
        self.requestHeaders = {} if requestParams is None else requestParams
        self.responseHeaders = {} if responseParams is None else responseParams
        self.version = None
        self.statusCode = StatusCode()
        self.body = ""
        if raw is not None:
            self.parseRaw(raw)
        if body is not None:
            self.body = body
            content = str(self.responseHeaders)
            self.responseHeaders['Content-Length'] = "157"
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
        assert len(data) == int(self.responseHeaders["Content-Length"])

    def parseContentLength(self, bodyHeadersLine):
        self.responseHeaders[bodyHeadersLine.split(":")[0]] = bodyHeadersLine.split(":")[1].strip()

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
               self.statusCode == other.statusCode
