from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot

from smoverlay.gui.qmonitor import QMonitor
from smoverlay.gui.qmlobject import QmlObject, qmlProperty
from .memory import MemoryMonitor

class QMemory(QmlObject):
    used = qmlProperty('quint64')
    free = qmlProperty('quint64')
    total = qmlProperty('quint64')
    percent = qmlProperty(float)

    def __init__(self, memory):
        QObject.__init__(self)
        self.update(memory)

    def update(self, memory):
        self.used = memory.used
        self.free = memory.free
        self.total = memory.total
        self.percent = memory.percent

class QMemoryMonitor(QMonitor):
    memory = qmlProperty(QMemory)

    def __init__(self):
        QMonitor.__init__(self, MemoryMonitor(), "Memory", "RCMemory.qml")
        self.qtypes_ += [QMemory]
        self.memory_ = QMemory(self.monitor.memory)

    @pyqtSlot()
    def update(self):
        QMonitor.update(self)
        self.memory.update(self.monitor.memory)

