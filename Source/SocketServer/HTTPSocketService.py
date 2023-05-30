import socket

from Source.Interfaces.SocketService import SocketService


class HTTPSocketService(SocketService):
    def __init__(self):
        self.connections = 0

    def serve(self, clientSocket=socket.socket()):
        request = clientSocket.recv(1024)
        content = """Harry Potter and the Sorcerer's Stone
J.K. Rowling
1999"""
        response = "HTTP/1.1 200 OK\n" + "Content-Length: " + \
                   str(len(content)) + "\n" + \
                   "\n" + \
                   content

        clientSocket.send(bytes(response,"UTF-8"))
        clientSocket.close()
        self.connections += 1
