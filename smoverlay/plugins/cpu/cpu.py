import psutil

from smoverlay.core.monitor import Monitor

class CPUMonitor(Monitor):
    def __init__(self, percpu=True):
        Monitor.__init__(self)
        self.percpu = percpu
        self.populate()

    def update(self, elapsed):
        self.cpus = psutil.cpu_percent(percpu=True)
        self.count = len(self.cpus)
        self.percent = sum(self.cpus) / self.count
