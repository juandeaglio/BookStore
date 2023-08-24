from Source.Interfaces.WebServerStrategy import WebServerStrategy
from Source.WebServerStrategy.GunicornStrategy import GunicornStrategy


class GunicornNginxStrategy(WebServerStrategy):
    def __init__(self, subprocessLib, osLibrary):
        super().__init__(subprocessLib, osLibrary)
        self.gunicorn = GunicornStrategy(subprocessLib, osLibrary)

    def start(self):
        self.gunicorn.start()
        if self.osLibrary.name == 'posix':
            return self.subprocessLib.Popen(['nginx', '-g daemon off'])

    def createStopCommand(self):
        cmd = ''

        if self.osLibrary.name == 'posix':
            cmd = "ps aux | egrep 'gunicorn|nginx|runserver' | grep 'BookStoreServer' | grep -v 'stopServer.py' " \
                  "| awk '{print $2}' | xargs -r kill -9"

        return cmd

    def isRunning(self):
        if self.osLibrary.name == 'posix':
            cmd = "CheckRunDjango.sh"
            cmd2 = "CheckRunGunicorn.sh"
            cmd3 = "CheckRunNginx.sh"
            return self.subprocessLib.run(["bash", cmd], capture_output=True).returncode > 0 and \
                self.subprocessLib.run(["bash", cmd2], capture_output=True).returncode > 0 and \
                self.subprocessLib.run(["bash", cmd3], capture_output=True).returncode > 0
