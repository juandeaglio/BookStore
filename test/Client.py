import socket


class Client:
    @staticmethod
    def createClientWithMessage(expectedMessage="", port=8091):
        client = Client.createClient(port)
        client.send(expectedMessage.encode("UTF-8"))
        return client

    @staticmethod
    def createClient(port):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(("localhost", port))
        return clientSocket
