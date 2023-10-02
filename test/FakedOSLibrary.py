import os


class FakedOSLibrary:
    def __init__(self, name=os.name):
        self.name = name

    @staticmethod
    def getcwd():
        return "D:/PyCharmProjs/BookStore"

    @staticmethod
    def popen(cmd):
        class Data:
            def read(self):
                return "localhost%20"

        return Data()
