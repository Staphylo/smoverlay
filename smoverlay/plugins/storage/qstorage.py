from PyQt5.QtCore import QObject, QVariant, pyqtSignal, pyqtProperty, pyqtSlot

from smoverlay.gui.qmonitor import QMonitor
from .storage import StorageMonitor

class QDisk(QObject):
    mountpointNotify = pyqtSignal()
    usepercentNotify = pyqtSignal()

    def __init__(self, mountpoint, usepercent):
        QObject.__init__(self)
        #self.declare('QString', 'mountpoint')
        #self.declare(float, 'usepercent')
        self.mountpoint_ = mountpoint
        self.usepercent_ = usepercent

    @pyqtProperty('QString', notify=mountpointNotify)
    def mountpoint(self):
        return self.mountpoint_

    @pyqtProperty(float, notify=usepercentNotify)
    def usepercent(self):
        return self.usepercent_

    def __str__(self):
        return "QDisk(%s)" % self.mountpoint_

class QStorageMonitor(QMonitor):
    def __init__(self):
        QMonitor.__init__(self, StorageMonitor(), "Storage", "RCStorage.qml") #"RCGroup.qml")
        self.qtypes_ += [QDisk]
        #self.disks = self.prop(list, fget=self.diskGet)
        #self.disks_ = QQmlListProperty(QDisk, self,
        #        append=lambda collec, item: item.setParentItem(collec))


    #@pyqtSlot()
    #def disks(self):

    disksChanged_ = pyqtSignal()
    @pyqtProperty(QVariant, notify=disksChanged_)
    #@pyqtProperty('QAbstractListModel', notify=disksChanged_)
    #@pyqtProperty(QAbstractListModel, notify=disksChanged_)
    #@pyqtProperty(ThingListModel, notify=disksChanged_)
    #@pyqtProperty('QQmlListProperty<Q>', notify=disksChanged_)
    #@pyqtProperty(QQmlListProperty, notify=disksChanged_)
    def disks(self):
        return self.disks_
        #return QQmlListProperty(QDisk, self,
        #        append=lambda collec, item: item.setParentItem(collec))

    @pyqtSlot()
    def update(self):
        QMonitor.update(self)
        #self.disks_ = ThingListModel([QDisk(mountpoint, data["usage"].percent) for mountpoint, data in self.monitor.disks.items()])
        #self.disks_ = [QDisk(mountpoint, data["usage"].percent) for mountpoint, data in self.monitor.disks.items()]
        #for mountpoint, data in self.monitor.disks.items():
        #    self.disks_.append(QDisk(mountpoint, data["usage"].percent))
        if not hasattr(self, 'disks_'):
            self.disks_ = [QDisk(mountpoint, data["usage"].percent)
                    for mountpoint, data in self.monitor.disks.items()]

        for disk in self.disks_:
            new = self.monitor.disks[disk.mountpoint_]["usage"].percent
            if disk.usepercent != new:
                disk.usepercent_ = new
                disk.usepercentNotify.emit()

        #self.disksChanged_.emit()
