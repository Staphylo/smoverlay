import time

class Monitor:
    def __init__(self):
        self.previousUpdate = 0
        self.config = {
            "refresh": 1
        }

    def autodetect(self):
        return { "refresh": 1 }

    def loadConfig(self, config):
        self.config = config

    def dumpConfig(self):
        return self.config

    def needUpdate(self, time):
        return time - self.previousUpdate >= self.config["refresh"]

    def _update(self, current):
        elapsed = current - self.previousUpdate
        self.previousUpdate = current
        self.update(elapsed)

    def update(self, elapsed):
        raise NotImplementedError("abstract class")

    def populate(self):
        self.update(time.monotonic())

