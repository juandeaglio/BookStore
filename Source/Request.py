from enum import Enum


class Method(Enum):
    GET = "GET",
    POST = "POST",
    OPTIONS = "OPTIONS"


class Request:
    def __init__(self, raw=""):
        self.method = ""
        self.path = ""
        self.version = ""
        if raw != "":
            self.parseRaw(raw)

    def parseRaw(self, raw):
        lines = raw.splitlines()
        iterator = iter(lines)

        headers = next(iterator).split(' ')
        self.setMethod(Method[headers[0]])
        self.path = headers[1][1:]
        self.version = headers[len(headers)-1]

    def setMethod(self, method):
        self.method = method.value
