import unittest
from unittest.mock import MagicMock

from Source.Server.Services.ClosingSocketService import ClosingSocketService
from Source.Server.HTTPServerFacade import HTTPServerFacade


class StoppingSocketTest(unittest.TestCase):
    def test_startAndStopServer(self):
        self.port = 8091
        webserver = MagicMock()
        self.server = HTTPServerFacade(webserver=webserver, port=self.port)
        self.server.start()
        assert self.server.isRunning()
        with self.assertRaises(SystemExit):
            self.server.stop()
        assert not self.server.isRunning()


if __name__ == '__main__':
    unittest.main()
