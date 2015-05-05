import psutil

from smoverlay.core.monitor import Monitor

class MemoryMonitor(Monitor):
    def __init__(self, monitorswap=True):
        Monitor.__init__(self)
        self.memory = None
        self.swap = None
        self.monitorswap = monitorswap
        self.populate()

    def update(self, elapsed):
        self.memory = psutil.virtual_memory()
        if self.monitorswap:
            self.swap = psutil.swap_memory()

