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
        if self.running:
            self.server_socket.close()
            self.running = False

    def acceptConnection(self):
        # TODO socket exception in BDD test case.
        while self.running:
            try:
                clientSocket, clientAddr = self.server_socket.accept()
                self.isServing = True
                self.service.serve(clientSocket)
                self.isServing = False
            except OSError as e:
                if e.errno == 10038 and self.running:
                    raise
    def getConnections(self):
        while self.isServing:
            pass
        return self.service.connections
