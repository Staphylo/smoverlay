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
        self.minPollInterval = min(monitor.pollInterval, self.minPollInterval)
        if monitor.name() in self.monitors:
            raise ValueError("monitor %s already present" % monitor.name())
        self.monitors[monitor.name()] = monitor

    @pyqtSlot('QString')
    def getMonitor(self, monitor):
        return self.monitors.get(monitor, None)

class QMonitor(QmlObject):
    monitor_name = qmlProperty('QString')
    monitor_view = qmlProperty('QString')
    updateInterval = qmlProperty(int)

    def __init__(self, mon, name, view):
        QObject.__init__(self)
        self.qtypes_ = [ self.__class__ ]
        self.monitor = mon
        self.monitor_view_ = "plugins/" + name.lower() + "/" + view
        self.monitor_name_ = name
        self.updateInterval_ = mon.pollInterval * 1000

    def types(self):
        return self.qtypes_

    def update(self):
        self.monitor._update(time.monotonic())

