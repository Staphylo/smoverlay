from PyQt5.QtCore import QObject, QVariant, pyqtSignal, pyqtProperty, pyqtSlot

from smoverlay.gui.qmonitor import QMonitor
from .network import NetworkMonitor

class QInterface(QObject):
    def __init__(self, name, info):
        QObject.__init__(self)
        self.name_ = name
        self.txspeed_ = info["txspeed"]
        self.rxspeed_ = info["rxspeed"]
        #self.type_ = # type of the interface
        #self.typedata_ = # data associated with the type
        #self.interfaces = Q

    nameChanged = pyqtSignal()
    @pyqtProperty('QString', notify=nameChanged)
    def name(self):
        return self.name_

    txspeedChanged = pyqtSignal()
    @pyqtProperty(float, notify=txspeedChanged)
    def txspeed(self):
        return self.txspeed_

    rxspeedChanged = pyqtSignal()
    @pyqtProperty(float, notify=rxspeedChanged)
    def rxspeed(self):
        return self.rxspeed_

    def update(self, name, info):
        if self.name_ != name:
            self.name_ = name
            self.nameChanged.emit()
        if self.txspeed_ != info["txspeed"]:
            self.txspeed_ = info["txspeed"]
            self.txspeedChanged.emit()
        if self.rxspeed_ != info["rxspeed"]:
            self.rxspeed_ = info["rxspeed"]
            self.rxspeedChanged.emit()

class QNetworkMonitor(QMonitor):
    interfacesChanged = pyqtSignal()

    def __init__(self):
        QMonitor.__init__(self, NetworkMonitor(), "Network", "RCNetwork.qml")
        self.qtypes_ += [QInterface]

    @pyqtProperty(QVariant, notify=interfacesChanged)
    def interfaces(self):
        return self.interfaces_

    @pyqtSlot()
    def update(self):
        QMonitor.update(self)
        if not hasattr(self, 'interfaces_'):
            self.interfaces_ = [ QInterface(name, info)
                    for name, info in self.monitor.interfaces.items() ]
        else:
            for iface, info in self.monitor.interfaces.items():
                data = [x for x in self.interfaces_ if x.name == iface]
                if not data:
                    self.interfaces_.append(QInterface(iface, info))
                    self.interfacesChanged.emit()
                else:
                    data = data[0]
                    data.update(iface, info)




