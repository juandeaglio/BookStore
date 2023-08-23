import os

from Source.Interfaces.WebServerStrategy import WebServerStrategy
import sys


class DjangoStrategy(WebServerStrategy):
    def createStopCommand(self):
        cmd = ''
        if os.name == 'nt':
            cmd = "Get-WmiObject Win32_Process | Where-Object " \
                  "{ $_.Name -match 'python' -and $_.CommandLine -like '*runserver*' } | " \
                  "ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
        elif os.name == 'posix':
            cmd = "ps aux | grep 'python' | grep 'runserver' | grep -v 'kill' | awk '{print $2}' | xargs -r kill -9"

        return cmd

    def isRunning(self, subprocessLib):
        cmd = ''
        if os.name == 'nt':
            # get all python processes and filter out the ones that are not runserver, count the number of processes and return true if there is at least one
            cmd = "CheckRunServerDjango.ps1"
            print(subprocessLib.run(["powershell", "-File", cmd], capture_output=True).returncode)
            return subprocessLib.run(["powershell", "-File", cmd], capture_output=True).returncode > 0

        elif os.name == 'posix':
            cmd = "CheckRunServer.sh"
            return subprocessLib.run(["bash", cmd], capture_output=True).returncode > 0

    def start(self, processLibrary):
        return processLibrary.Popen([sys.executable, "startDjangoWithTestUser.py"])
