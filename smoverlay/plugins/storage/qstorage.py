from PyQt5.QtCore import QVariant

from smoverlay.gui.qmonitor import QMonitor
from smoverlay.gui.qmlobject import QmlObject, QObject, pyqtSlot, qmlProperty
from .storage import StorageMonitor

class QDisk(QmlObject):
    mountpoint = qmlProperty(str)
    usepercent = qmlProperty(float)

    def __init__(self, mountpoint, usepercent):
        QObject.__init__(self)
        self.mountpoint = mountpoint
        self.usepercent = usepercent

class QStorageMonitor(QMonitor):
    disks = qmlProperty(QVariant)

    def __init__(self):
        QMonitor.__init__(self, StorageMonitor(), "Storage", "storage.qml")
        self.monitorHeight_ = 0
        self.qtypes_ += [QDisk]

    @pyqtSlot()
    def update(self):
        QMonitor.update(self)
        if not hasattr(self, 'disks_'):
            self.disks_ = [QDisk(mountpoint, data["usage"].percent)
                    for mountpoint, data in self.monitor.disks.items()]

        for disk in self.disks_:
            new = self.monitor.disks[disk.mountpoint]["usage"].percent
            disk.usepercent = new
        self.monitorHeight_ = 30 * len(self.disks_)
