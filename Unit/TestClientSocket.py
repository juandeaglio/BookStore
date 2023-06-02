class TestClientSocket:
    def recv(self, __bufsize: int, __flags: int = ...) -> bytes:
        return bytes("\r\n\r\n", "UTF-8")

    def send(self, data):
        pass

    def close(self) -> None:
        pass
