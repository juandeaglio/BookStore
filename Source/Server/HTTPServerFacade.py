import signal
from flask import Flask
import threading

from Source.Interfaces.Server import Server


class HTTPServerFacade(Server):
    def __init__(self, port=8091, webserver=Flask):
        self.serverThread = threading.Thread()
        self.running = False
        self.app = webserver(__name__)
        self.port = port

    def start(self):
        self.serverThread = threading.Thread(target=lambda: self.app.run(debug=False, use_reloader=False))
        self.serverThread.start()
        self.running = True

    def stop(self):
        self.serverThread.join(timeout=0.5)
        self.running = False
        raise SystemExit

    def isRunning(self):
        return self.running

    def getConnections(self):
        pass
