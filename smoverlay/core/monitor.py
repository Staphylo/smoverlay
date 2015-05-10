import time

class Monitor:
    def __init__(self):
        self.pollInterval = 1.
        self.previousUpdate = 0
        self.config = {}

    def autodetect(self):
        return { "refresh": self.pollInterval }

    def loadConfig(self, config):
        self.config = config

    def dumpConfig(self):
        return self.config

    def refreshEvery(self, seconds):
        self.pollInterval = seconds

    def needUpdate(self, time):
        return time - self.previousUpdate >= self.pollInterval

    def _update(self, current):
        elapsed = current - self.previousUpdate
        self.previousUpdate = current
        self.update(elapsed)

    def update(self, elapsed):
        raise NotImplementedError("abstract class")

    def populate(self):
        self.update(time.monotonic())

