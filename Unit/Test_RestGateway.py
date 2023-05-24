import unittest

from Source.RestMessage import RestMessage
from Source.EchoRestGateway import EchoRestGateway


class MyTestCase(unittest.TestCase):
    def test_canReceiveEmpty(self):
        expectedMessage = RestMessage(method="GET",path="/")
        self.gateway = EchoRestGateway()
        assert expectedMessage == self.gateway.getMessageFromQueue()


if __name__ == '__main__':
    unittest.main()
