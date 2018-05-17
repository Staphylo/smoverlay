from PyQt5.QtCore import QObject, QVariant, pyqtSlot

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

    datapoints = qmlProperty(int)
    maxspeed = qmlProperty(float)
    # XXX QQmlListProperty ?
    rxspeed = qmlProperty(QVariant)
    txspeed = qmlProperty(QVariant)

    def __init__(self):
        QMonitor.__init__(self, NetworkMonitor(), "Network", "network.qml")
        self.monitorHeight_ = 0

        self.datapoints_ = 20
        self.maxspeed_ = 0
        self.rxspeed_ = [0] * self.datapoints_
        self.txspeed_ = [0] * self.datapoints_
        self.qtypes_ += [QInterface]

    @pyqtSlot()
    def update(self):
        QMonitor.update(self)
        rx = 0
        tx = 0
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
                rx += info["rxspeed"]
                tx += info["txspeed"]
        self.rxspeed[:] = self.rxspeed[1:] + [rx]
        self.txspeed[:] = self.txspeed[1:] + [tx]
        self.maxspeed = max(max(self.rxspeed), max(self.txspeed))
        self.monitorHeight = len(self.monitor.interfaces) * 32 + 50




