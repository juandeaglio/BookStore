import socket

from Source.Interfaces.SocketService import SocketService


class HTTPSocketService(SocketService):
    def __init__(self, catalog):
        self.lastResponse = None
        self.catalog = catalog
        self.connections = 0

    def serve(self, clientSocket=socket.socket()):
        self.discardRequest(clientSocket)

        content = self.catalog.toString()
        response = "HTTP/1.1 200 OK\n" + \
                   "Access-Control-Allow-Origin: *\n" + \
                   "Content-Type: text/plain\n" + \
                   "Content-Length: " + \
                   str(len(content)) + "\n" + \
                   "\n" + \
                   content

        clientSocket.send(bytes(response, "UTF-8"))
        self.lastResponse = bytes(response, "UTF-8")
        clientSocket.close()

        self.connections += 1

    def discardRequest(self, clientSocket):
        page = ""
        while "\r\n\r\n" not in page:
            buf = clientSocket.recv(1024).decode("UTF-8")
            page += buf
