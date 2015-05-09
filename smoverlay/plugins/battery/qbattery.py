from PyQt5.QtCore import QObject, pyqtSlot

from smoverlay.gui.qmonitor import QMonitor
from smoverlay.gui.qmlobject import QmlObject, qmlProperty
from .battery import BatteryMonitor

class QBatteryMonitor(QMonitor):
    percent = qmlProperty(float)
    status = qmlProperty('QString')

    def __init__(self):
        QMonitor.__init__(self, BatteryMonitor(), "Battery", "RCBattery.qml")

    @pyqtSlot()
    def update(self):
        QMonitor.update(self)
        self.percent = self.monitor.percent
        self.status = self.monitor.status

