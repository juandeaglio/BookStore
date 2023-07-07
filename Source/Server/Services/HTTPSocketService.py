import socket
from Source.Interfaces.SocketService import SocketService
from Source.Request import Request
from Source.Response import Response


class HTTPSocketService(SocketService):
    def __init__(self, catalog):
        self.lastResponse = None
        self.catalog = catalog
        self.connections = 0

    def serve(self, clientSocket=socket.socket()):

        content, contentType = self.routeRequest(clientSocket)
        response = "HTTP/1.1 200 OK\n" + \
                   "Access-Control-Allow-Origin: *\n" + \
                   "Content-Type: " + contentType + "\n" + \
                   "Content-Length: " + \
                   str(len(content)) + "\n" + \
                   "\n" + \
                   content

        clientSocket.send(bytes(response, "UTF-8"))
        self.lastResponse = bytes(response, "UTF-8")
        clientSocket.close()

        self.connections += 1
        return

    def discardRequest(self, clientSocket):
        self.receiveHTTP(clientSocket)

    def routeRequest(self, clientSocket):
        content = ""
        contentType = ""
        request = Request(raw=self.receiveHTTP(clientSocket))
        if request.path == "about":
            content = open("./Source/Static/about.html", "r").read()
            contentType = "text/html"
        elif request.path == 'getCatalog':
            content = self.catalog.toString()
            contentType = "text/plain"

        return content, contentType

    def receiveHTTP(self, clientSocket):
        http = ""
        while "\r\n\r\n" not in http:
            buf = clientSocket.recv(1024).decode("UTF-8")
            http += buf
        return http
