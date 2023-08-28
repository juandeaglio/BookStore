from Source.Interfaces.WebServerStrategy import WebServerStrategy


class GunicornStrategy(WebServerStrategy):
    def __init__(self, subprocessLib, osLibrary, ports=None):
        super().__init__(subprocessLib, osLibrary, ports=ports)

    def start(self):
        port = 8091
        if self.ports.get('gunicornPort'):
            port = self.ports.get('gunicornPort')

        if self.osLibrary.name == 'posix':
            return self.subprocessLib.Popen(["gunicorn", "-b", "0.0.0.0:"+str(port), "BookStoreServer.wsgi"])

    def createStopCommand(self):
        cmd = ''

        if self.osLibrary.name == 'posix':
            cmd = "ps aux | grep 'gunicorn' | grep 'BookStoreServer' | grep -v 'stopServer.py'  | awk '{print $2}' " \
                  "| xargs -r kill -9"

        return cmd

    def isRunning(self):
        if self.osLibrary.name == 'posix':
            cmd2 = "CheckRunGunicorn.sh"
            return self.subprocessLib.run(["bash", cmd2], capture_output=True).returncode > 0
