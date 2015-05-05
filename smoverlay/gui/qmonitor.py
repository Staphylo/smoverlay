import sys
import os
import psutil
import time

from PyQt5.QtCore import *

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

class QMixinProperty(object):
    def __init__(self, value):
        self.value = value

    def __set__(self, obj, value):
        self.value = value

    def __get__(self, obj, objtype=None):
        return self.value

    def __changed__(self):
        print("changed")

class QMonitor(QObject):
    def prop(self, *args, signal=None, notify=None, **kwargs):
        if notify:
            if not signal:
                signal = pyqtSignal()
            #signal.connect(notify)
            return pyqtProperty(*args, notify=signal, **kwargs)
        return pyqtProperty(*args, **kwargs)

    def encaps(self, name, typ, value, fget=True, fset=True, **kwargs):
        if fset:
            def fset(self, value):
                setattr(self, name, value)
            setattr(self, "set_%s" % name, fset)
        if fget:
            def fget(self):
                return getattr(self, name)
            setattr(self, "get_%s" % name, fget)
        p = self.prop(typ, fget=fget, fset=fset, **kwargs)
        p = value
        return p

    def __init__(self, mon, name, view):
        QObject.__init__(self)
        #self.name = self.encaps('count', 'QString', name, fset=None)
        #self.monitor = self.encaps('monitor', mon.__class__, mon, fset=None)
        ##self.view = self.encaps('view', 'QString', view, fset=None)
        #self.view = self.encaps('view', 'QString', view, fset=None)

        self.qtypes_ = [ self.__class__ ]
        self.monitor = mon
        self.monitor_view_ = "plugins/" + name.lower() + "/" + view
        self.monitor_name_ = name
        self.updateInterval_ = mon.pollInterval * 1000

    def types(self):
        return self.qtypes_

    updateIntervalChanged = pyqtSignal()
    @pyqtProperty(int, notify=updateIntervalChanged)
    def updateInterval(self):
        return self.updateInterval_

    @pyqtProperty('QString')
    def monitor_view(self):
        return self.monitor_view_

    @pyqtProperty('QString')
    def monitor_name(self):
        return self.monitor_name_

    @pyqtSlot()
    def update(self):
        self.monitor._update(time.monotonic())

