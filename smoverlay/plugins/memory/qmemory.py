from smoverlay.gui.qmonitor import QMonitor
from smoverlay.gui.qmlobject import QmlObject, QObject, qmlProperty, pyqtSlot
from .memory import MemoryMonitor

class QMemory(QmlObject):
    label = qmlProperty('QString')
    used = qmlProperty('quint64')
    free = qmlProperty('quint64')
    total = qmlProperty('quint64')
    percent = qmlProperty(float)

    def __init__(self, memory, label):
        QObject.__init__(self)
        self.label_ = label
        self.update(memory)

    def update(self, memory):
        self.used = memory.used
        self.free = memory.free
        self.total = memory.total
        self.percent = memory.percent

class QMemoryMonitor(QMonitor):
    memory = qmlProperty(QMemory)
    swap = qmlProperty(QMemory)
    hasSwap = qmlProperty(bool)

    def __init__(self):
        QMonitor.__init__(self, MemoryMonitor(), "Memory", "memory.qml")
        self.qtypes_ += [QMemory]
        self.memory_ = QMemory(self.monitor.memory, "RAM")
        self.hasSwap_ = self.monitor.monitorswap
        self.swap_ = QMemory(self.monitor.swap, "SWAP")

    @pyqtSlot()
    def update(self):
        QMonitor.update(self)
        self.memory.update(self.monitor.memory)
        if self.hasSwap_:
            self.swap.update(self.monitor.swap)
        self.monitorHeight = 60 if self.monitor.monitorswap else 30

