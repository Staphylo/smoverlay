from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot

from smoverlay.gui.qmonitor import QMonitor
from smoverlay.gui.qmlobject import QmlObject, qmlProperty
from .volume import VolumeMonitor

class QVolumeMonitor(QMonitor):
    volume = qmlProperty(int, 'volumeChanged')
    muted = qmlProperty(bool, 'mutedChanged')

    def __init__(self):
        QMonitor.__init__(self, VolumeMonitor(), "Volume", "volume.qml")
        self.muted_ = False
        self.volume_ = 0

    def volumeChanged(self, volume):
        print("new volume:", volume)

    def mutedChanged(self, muted):
        print("toggle mute")
