from PyQt5.QtCore import QVariant

from smoverlay.gui.qmonitor import QMonitor
from smoverlay.gui.qmlobject import QmlObject, QObject, qmlProperty, pyqtSlot
from .memory import MemoryMonitor

class QMemory(QmlObject):
    label = qmlProperty('QString')
    used = qmlProperty('quint64')
    free = qmlProperty('quint64')
    total = qmlProperty('quint64')
    percent = qmlProperty(float)

    def __init__(self, label, memory):
        QObject.__init__(self)
        self.label_ = label
        self.update(memory)

    def update(self, memory):
        self.used = memory.used
        self.free = memory.free
        self.total = memory.total
        self.percent = memory.percent

class QMemoryMonitor(QMonitor):
    memories = qmlProperty(QVariant)

    def __init__(self):
        QMonitor.__init__(self, MemoryMonitor(), "Memory", "memory.qml")
        self.qtypes_ += [QMemory]
        ram = QMemory("RAM", self.monitor.memory)
        swap = QMemory("SWAP", self.monitor.swap)
        self.hasSwap = self.monitor.monitorswap
        self.memories = [ram, swap] if self.hasSwap else [ram]
        self.monitorHeight = 60 if self.hasSwap else 30

    @pyqtSlot()
    def update(self):
        QMonitor.update(self)
        self.memories[0].update(self.monitor.memory)
        if self.hasSwap:
            self.memories[1].update(self.monitor.swap)

