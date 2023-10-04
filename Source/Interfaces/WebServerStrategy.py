from abc import ABC, abstractmethod


class WebServerStrategy(ABC):
    def __init__(self, sub_process_library, os_library, ports=None):
        self.sub_process_lib = sub_process_library
        self.os_library = os_library
        self.ports = ports or {}

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def create_stop_command(self):
        pass

    @abstractmethod
    def is_running(self):
        pass
