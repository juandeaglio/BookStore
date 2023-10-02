from test.FakeProcess import FakeProcess


class FakedProcessLibrary:
    def run(self, args=None, capture_output=True, check=True):
        class ProcResults:
            returncode = 0
            stdout = bytes("localhost", encoding='utf-8')

        return ProcResults()

    def call(self):
        pass

    def Popen(self, args=None):
        if args is None:
            args = []

        return FakeProcess()
