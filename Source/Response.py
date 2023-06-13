import io


class StatusCode:
    def __init__(self):
        self.number = -1
        self.message = ""


class Response:
    def __init__(self, body=None, raw=None):
        self.requestHeaders = {"Access-Control-Allow-Origin": ""}
        self.responseHeaders = {"Content-Type": "", "Content-Length": 0}
        self.version = None
        self.statusCode = StatusCode()
        self.body = ""
        if raw is not None:
            self.parseRaw(raw)
        if body is not None:
            self.body = body
            self.contentLength = len(self.body)

    def parseRaw(self, rawBytes):
        byteData = io.StringIO(rawBytes.decode("UTF-8"))
        self.parseStartLine(byteData)
        bodyHeadersLine = self.parseRequestHeaders(byteData)
        body = self.parseResponseHeaders(bodyHeadersLine, byteData)
        self.parseContentLength(body)
        assert byteData.readline() == '\n'
        self.parseBody(byteData)

    def parseBody(self, byteData):
        self.body = byteData.read()
        length = len(self.body)
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
        headers[header[0]] = header[1]
        requestHeadersLine = byteData.readline().strip()
        return requestHeadersLine

    def parseStartLine(self, byteData):
        startLine = byteData.readline().strip()
        self.version = startLine.split(" ")[0]
        self.statusCode.number = int(startLine.split(" ")[1])
        self.statusCode.message = startLine.split(" ")[1] + " " + startLine.split(" ")[2]
