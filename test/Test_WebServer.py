import unittest
from Source.WebServer import WebServer


class FakedOSLibrary:
    def __init__(self):
        self.name = 'None'


class FakedProcessLibrary:
    def run(self):
        pass

    def call(self):
        pass

    def Popen(self, args=None):
        if args is None:
            args = []


class TestWebServer(unittest.TestCase):
    pass