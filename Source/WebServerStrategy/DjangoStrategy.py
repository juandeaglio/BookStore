import os

from Source.Interfaces.WebServerStrategy import WebServerStrategy
import sys


class DjangoStrategy(WebServerStrategy):
    def __init__(self, sub_process_library, os_library, ports=None):
        super().__init__(sub_process_library, os_library, ports=ports)

    def create_stop_command(self):
        cmd = ''
        if os.name == 'nt':
            cmd = "Get-WmiObject Win32_Process | Where-Object " \
                  "{ $_.Name -match 'python' -and $_.CommandLine -like '*runserver*' } | " \
                  "ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
        elif os.name == 'posix':
            cmd = "ps aux | grep 'python' | grep 'runserver' | grep -v 'kill' | awk '{print $2}' | xargs -r kill -9"

        return cmd

    def is_running(self):
        cmd = ''
        if os.name == 'nt':
            # get all python processes and filter out the ones that are not runserver, count the number of processes and return true if there is at least one
            cmd = "./Source/Scripts/CheckRunServerDjango.ps1"
            print(self.sub_process_lib.run(["powershell", "-File", cmd], capture_output=True).returncode)
            return self.sub_process_lib.run(["powershell", "-File", cmd], capture_output=True).returncode > 0

        elif os.name == 'posix':
            cmd = "./Source/Scripts/CheckRunDjango.sh"
            return self.sub_process_lib.run(["bash", cmd], capture_output=True).returncode > 0

    def start(self):
        return self.sub_process_lib.Popen([sys.executable, "./startDjangoWithTestUser.py"])
