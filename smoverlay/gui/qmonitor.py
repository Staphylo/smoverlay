import sys
import os
import psutil
import time

from PyQt5.QtCore import *
from smoverlay.gui.qmlobject import QmlObject, qmlProperty

class QMonitorManager(QObject):
    def __init__(self):
        self.monitors = []

    def add(self, monitor):
        if monitor.name() in self.monitors:
            raise ValueError("monitor %s already present" % monitor.name())
        self.monitors[monitor.name()] = monitor

    @pyqtSlot('QString')
    def getMonitor(self, monitor):
        return self.monitors.get(monitor, None)

class QMonitor(QmlObject):
    monitorName = qmlProperty('QString')
    monitorView = qmlProperty('QString')
    monitorHeight = qmlProperty(int)
    updateInterval = qmlProperty(int)

    def __init__(self, mon, name, view):
        QObject.__init__(self)
        self.qtypes_ = [ self.__class__ ]
        self.monitor = mon
        self.monitorView_ = "../../plugins/" + name.lower() + "/" + view
        self.monitorName_ = name
        self.updateInterval_ = mon.config["refresh"] * 1000
        if "height" in mon.config:
            self.monitorHeight = mon.config.setdefault("height", 100)

    def loadConfig(self, config):
        self.monitor.loadConfig(config)
        #print(self.__class__.__name__, self.monitor.config)
        self.updateInterval = self.monitor.config["refresh"] * 1000
        if "height" in self.monitor.config:
            self.monitorHeight = self.monitor.config["height"]

    #def defaultConfig(self):
    #    default = self.monitor.defaultConfig()
    #    default["height"] = 1000
    #    return default

    def fieldInitialized(self, name):
        return hasattr(self, name + '_')

    def types(self):
        return self.qtypes_

    def update(self):
        self.monitor._update(time.monotonic())

