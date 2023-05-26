from Source.Interfaces.SocketService import SocketService


class RestSocketService(SocketService):
    def serve(self, socket):
        pass

    def __init__(self, bookStore):
        self.bookStore = bookStore
