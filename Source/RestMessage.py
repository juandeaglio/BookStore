class RestMessage:
    def __init__(self, method=None, path=None, body=None, rawMsg=None):
        self.method = method
        self.path = path
        self.body = body
        self.rawMsg = rawMsg

    def __eq__(self, other):
        return True
