import socket

from Source.Interfaces.SocketService import SocketService


class HTTPSocketService(SocketService):
    def __init__(self, bookStore):
        self.bookStore = bookStore
        self.connections = 0

    def serve(self, clientSocket=socket.socket()):
        page = ""
        while "\r\n\r\n" not in page:
            buf = clientSocket.recv(1024).decode("UTF-8")
            page += buf
        content = self.bookStore.getCatalogToString()
        response = "HTTP/1.1 200 OK\n" + "Content-Length: " + \
                   str(len(content)) + "\n" + \
                   "\n" + \
                   content

        clientSocket.send(bytes(response, "UTF-8"))
        clientSocket.close()
        self.connections += 1
