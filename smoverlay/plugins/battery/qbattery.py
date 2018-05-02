from PyQt5.QtCore import QObject, QVariant, pyqtSlot

from smoverlay.gui.qmonitor import QMonitor
from smoverlay.gui.qmlobject import QmlObject, qmlProperty
from .battery import BatteryMonitor

class QBattery(QmlObject):
    percent = qmlProperty(float)
    label = qmlProperty('QString')
    status = qmlProperty('QString')

    def __init__(self, label, *args):
        QObject.__init__(self)
        self.label = str(label)
        self.update(*args)

    def update(self, percent, status):
        self.percent = percent
        self.status = status

class QBatteryMonitor(QMonitor):
    batteries = qmlProperty(QVariant)
    # remaining

    def __init__(self):
        QMonitor.__init__(self, BatteryMonitor(), "Battery", "battery.qml")
        self.qtypes_ += [QBattery]
        self.monitorHeight_ = 0

    @pyqtSlot()
    def update(self):
        QMonitor.update(self)
        batteries = self.monitor.batteries
        if not self.fieldInitialized('batteries'):
            self.batteries = [QBattery(bat.uid, bat.percent, bat.status)
                              for bat in batteries]
        else:
            for battery, bat in zip(self.batteries, batteries):
                battery.update(bat.percent, bat.status)
        self.monitorHeight_ = 40 * len(self.batteries)

