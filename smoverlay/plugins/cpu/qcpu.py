from PyQt5.QtCore import QVariant

from smoverlay.gui.qmonitor import QMonitor
from smoverlay.gui.qmlobject import QmlObject, QObject, qmlProperty, pyqtSlot
from .cpu import CPUMonitor

class QCPU(QmlObject):
    percent = qmlProperty(float)
    def __init__(self, percent):
        QObject.__init__(self)
        self.percent = percent

class QCPUMonitor(QMonitor):
    percent = qmlProperty(float)
    count = qmlProperty(int)
    cpus = qmlProperty(QVariant)

    def __init__(self):
        QMonitor.__init__(self, CPUMonitor(), "CPU", "cpu.qml")
        self.qtypes_ += [QCPU]
        self.monitorheight_ = 0
        self.percent_ = 0
        self.count_ = 0
        print(self.monitor.config)

    def fieldInitialized(self, name):
        return hasattr(self, name + '_')

    @pyqtSlot()
    def update(self):
        QMonitor.update(self)
        self.percent = self.monitor.percent
        self.count = self.monitor.count
        #print(self.percent,self.monitor.cpus)
        cpus = self.monitor.cpus.copy()
        cpus.sort(reverse=True)
        if not self.fieldInitialized('cpus'):
            self.cpus = [QCPU(percent) for percent in cpus]
        else:
            for cpu, percent in zip(self.cpus, cpus):
                cpu.percent = percent
        self.monitorHeight = 65

