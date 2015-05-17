
from smoverlay.core.monitor import Monitor

PLUGIN_SKIP = True

class VolumeMonitor(Monitor):
    def __init__(self):
        Monitor.__init__(self)

    def update(self, elapsed):
        pass
