import socket
import threading


class SimpleSocketServer:
    def __init__(self, port=8091, service=None):
        self.isServing = False
        self.clientThreads = []
        self.port = port
        self.service = service
        self.running = False
        self.server_socket = socket.socket()

    def start(self):
        self.runAsServer(self.server_socket)

        clientThread = threading.Thread(target=self.acceptConnection)
        clientThread.start()
        self.clientThreads.append(clientThread)

    def runAsServer(self, server_socket):
        server_socket.bind(("localhost", self.port))
        server_socket.listen()
        self.running = True

    def acceptConnection(self):
        # TODO socket exception in BDD test case.
        while self.running:
            self.handleNextClient()

    def handleNextClient(self):
        try:
            clientSocket, clientAddr = self.server_socket.accept()
            self.isServing = True
            self.service.serve(clientSocket)
            self.isServing = False

        except OSError as e:
            if e.errno == 10038 and self.running:
                raise

    def isRunning(self):
        return self.running

    def stop(self):
        if self.running:
            self.server_socket.close()
            self.running = False

    def getConnections(self):
        while self.isServing:
            pass
        return self.service.connections
