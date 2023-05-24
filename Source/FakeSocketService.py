from Source.Interfaces.SocketService import SocketService


class FakeSocketService(SocketService):
    def __init__(self):
        super().__init__()

    def serve(self, socket):
        super().serve(socket)
        self.connections = super().connections
