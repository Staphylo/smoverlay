import time
import sys

from smoverlay.plugins import monitors

class Manager:
    def __init__(self):
        self.monitors = []
        self.minPollInterval = 1000

    def add(self, monitor):
        self.minPollInterval = min(monitor.pollInterval, self.minPollInterval)
        self.monitors.append(monitor)

    def run(self):
        while True:
            current = time.monotonic()
            for monitor in self.monitors:
                if monitor.needUpdate(current):
                    monitor._update(current)
                __import__("pprint").pprint(monitor.__dict__)
            # dummy system
            time.sleep(self.minPollInterval - (time.monotonic() - current))

def main():
    global monitors
    #sm = StorageMonitor()
    sm = monitors["storage"]()
    sm.refreshEvery(1.)
    for mnt in [ "/", "/tmp" ]:
        sm.watch(mnt)

    #nm = NetworkMonitor()
    nm = monitors["network"]()
    #mm = MemoryMonitor()
    mm = monitors["memory"]()

    monitors = [ sm, nm, mm ]

    m = Manager()
    for monitor in monitors:
        m.add(monitor)
    m.run()
    return 0

if __name__ == '__main__':
    sys.exit(main())
