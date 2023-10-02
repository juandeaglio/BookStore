class FakeProcess:
    def terminate(self):
        pass

    def kill(self):
        pass

    def poll(self):
        return None
