import logging
import socket

from Source.Interfaces.SocketService import SocketService


class ClosingSocketService(SocketService):
    def __init__(self):
        self.connections = 0

    def serve(self, clientSocket=socket.socket()):
        clientSocket.close()
        self.connections += 1
