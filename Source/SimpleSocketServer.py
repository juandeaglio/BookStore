from Source.Interfaces.SocketService import SocketService
import socket
import threading

class SimpleSocketServer:
    def __init__(self,  port=None, service=None):
        self.port = port
        self.service = service
        self.running = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("localhost", self.port))
        self.server_socket.listen()
        clientThread = threading.Thread(target=self.acceptConnection)
        clientThread.start()
        self.running = True

    def isRunning(self):
        return self.running

    def stop(self):
        self.server_socket.close()
        self.running = False

    def acceptConnection(self):
        try:
            clientSocket, clientAddr = self.server_socket.accept()
            self.service.serve(clientSocket)

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)

