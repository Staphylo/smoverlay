"""
Usage: smoverlay-cli [--debug] [--config filename] [--info] [--write]

Options:
    --debug             add verbosity
    --config filename   load this configuration file [default: ~/.smoverlayrc]
    --info              display information
"""

import os
import sys
import time
import yaml

from collections import OrderedDict
from functools import wraps
from docopt import docopt

from smoverlay.plugins import monitors
from smoverlay.core.config import loadConfig, generateConfig, dumpConfig

docstring = __doc__

class Manager:
    debug = False

    def __init__(self):
        self.monitors = []
        self.minPollInterval = 1000

    def add(self, monitor):
        self.minPollInterval = min(monitor.config["refresh"], self.minPollInterval)
        self.monitors.append(monitor)

    def run(self):
        while True:
            current = time.monotonic()
            for monitor in self.monitors:
                if monitor.needUpdate(current):
                    monitor._update(current)
                if Manager.debug:
                    __import__("pprint").pprint(monitor.__dict__)
            # dummy system
            time.sleep(self.minPollInterval - (time.monotonic() - current))

def information():
    print("Plugin loaded:")
    for name, cls in monitors.items():
        print(" - %s (%s)" % (name, cls))

def main():
    args = docopt(docstring, version=smoverlay.core.config.version)

    dumpconfig = False
    print(args)
    if args["--info"]:
        information()
        return 0
    if args["--debug"]:
        Manager.debug = True
    if args["--write"]:
        dumpconfig = True

    config = loadConfig(args["--config"])
    if not config:
        config = generateConfig()
        if dumpconfig:
            dumpConfig(args["--config"], config)

    m = Manager()
    for plugin in config["plugins"]:
        (name, data) = plugin.popitem()
        mon = monitors[data["plugin"]]()
        mon.loadConfig(data["config"])
        m.add(mon)
    m.run()

    return 0

if __name__ == '__main__':
    sys.exit(main())
