class TestClientSocket:
    def __init__(self, path):
        self.path = path
    def recv(self, __bufsize: int, __flags: int = ...) -> bytes:
        return bytes("GET " + self.path + " \r\n\r\n", "UTF-8")

    def send(self, data):
        pass

    def close(self) -> None:
        pass
