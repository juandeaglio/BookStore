from Source.Interfaces.WebServerStrategy import WebServerStrategy


class GunicornStrategy(WebServerStrategy):
    def __init__(self, subprocessLib, osLibrary):
        super().__init__(subprocessLib, osLibrary)

    def start(self):
        if self.osLibrary.name == 'posix':
            return self.subprocessLib.Popen(["gunicorn", "-b", "0.0.0.0:8091", "BookStoreServer.wsgi"])

    def createStopCommand(self):
        cmd = ''

        if self.osLibrary.name == 'posix':
            cmd = "ps aux | grep 'gunicorn' | grep 'BookStoreServer' | grep -v 'stopServer.py'  | awk '{print $2}' " \
                  "| xargs -r kill -9"

        return cmd

    def isRunning(self):
        if self.osLibrary.name == 'posix':
            cmd = "CheckRunServer.sh"
            return self.subprocessLib.run(["bash", cmd], capture_output=True).returncode > 0
