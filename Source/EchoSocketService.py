import socket

from Source.Interfaces.SocketService import SocketService


class EchoSocketService(SocketService):
    def __init__(self):
        self.connections = 0

    def serve(self, clientSocket=socket.socket()):
        clientSocket.send(clientSocket.recv(1024))
        clientSocket.close()
        self.connections += 1
