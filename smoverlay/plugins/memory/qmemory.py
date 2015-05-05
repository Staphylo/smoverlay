from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot

from smoverlay.gui.qmonitor import QMonitor
from .memory import MemoryMonitor

class QMemory(QObject):
    usedChanged = pyqtSignal()
    totalChanged = pyqtSignal()
    percentChanged = pyqtSignal()

    def __init__(self, memory):
        QObject.__init__(self)
        self.total_ = memory.total
        self.free_ = memory.free
        self.used_ = memory.used
        self.percent_ = memory.percent

    @pyqtProperty('quint64')
    def free(self):
        return self.free_

    #@pyqtProperty(int)
    @pyqtProperty('quint64', notify=totalChanged)
    def total(self):
        return self.total_

    @pyqtProperty('quint64', notify=usedChanged)
    def used(self):
        return self.used_

    @pyqtProperty(float, notify=percentChanged)
    def percent(self):
        return self.percent_

    def update(self, memory):
        if self.total_ != memory.total:
            self.total_ = memory.total
            self.totalChanged.emit()
        if self.percent_ != memory.percent:
            self.percent_ = memory.percent
            self.percentChanged.emit()
        if self.used_ != memory.used:
            self.used_ = memory.used
            self.usedChanged.emit()

class QMemoryMonitor(QMonitor):
    memoryChanged_ = pyqtSignal()

    def __init__(self):
        QMonitor.__init__(self, MemoryMonitor(), "Memory", "RCMemory.qml")
        self.qtypes_ += [QMemory]
        self.memory_ = QMemory(self.monitor.memory)

    #@pyqtSlot()
    @pyqtProperty(QMemory, notify=memoryChanged_)
    def memory(self):
        return self.memory_

    @pyqtSlot()
    def update(self):
        QMonitor.update(self)
        # XXX new instance
        self.memory_.update(self.monitor.memory)
        #self.memoryChanged_.emit()

