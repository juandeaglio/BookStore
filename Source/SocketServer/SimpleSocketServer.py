import socket
import threading


class SimpleSocketServer:
    def __init__(self, port=8091, service=None):
        self.isServing = False
        self.clientThreads = []
        self.port = port
        self.service = service
        self.running = False
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("localhost", self.port))
        self.server_socket.listen()
        self.running = True
        clientThread = threading.Thread(target=self.acceptConnection)
        clientThread.start()
        self.clientThreads.append(clientThread)

    def isRunning(self):
        return self.running

    def stop(self):
        self.server_socket.close()
        self.running = False

    def acceptConnection(self):
        while self.running:
            clientSocket, clientAddr = self.server_socket.accept()
            self.isServing = True

            self.service.serve(clientSocket)
            self.isServing = False

    def getConnections(self):
        while self.isServing:
            pass
        return self.service.connections

    def waitToStart(self):
        while not self.running:
            pass
        return self.running
