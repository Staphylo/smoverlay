from PyQt5.QtCore import QObject, QVariant, pyqtSignal, pyqtProperty, pyqtSlot

from smoverlay.gui.qmonitor import QMonitor
from smoverlay.gui.qmlobject import QmlObject, qmlProperty
from .network import NetworkMonitor

class QInterface(QmlObject):
    name = qmlProperty('QString')
    txspeed = qmlProperty(float)
    rxspeed = qmlProperty(float)

    def __init__(self, name, info):
        QObject.__init__(self)
        self.name_ = name
        self.txspeed_ = info["txspeed"]
        self.rxspeed_ = info["rxspeed"]

    def update(self, name, info):
        self.name = name
        self.txspeed = info["txspeed"]
        self.rxspeed = info["rxspeed"]

class QNetworkMonitor(QMonitor):
    interfaces = qmlProperty(QVariant)

    def __init__(self):
        QMonitor.__init__(self, NetworkMonitor(), "Network", "RCNetwork.qml")
        self.qtypes_ += [QInterface]

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
                    self.interfacesChanged.emit(self.interfaces_)
                else:
                    data = data[0]
                    data.update(iface, info)




