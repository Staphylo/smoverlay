import socket
import struct
import array
import fcntl

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSlot, pyqtSignal

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
maxLength = {
    "interface": 16,
    "essid": 32
}
calls = {
    "SIOCGIWESSID": 0x8B1B
}

def getEssid(interface):
    """Return the ESSID for an interface, or None if we aren't connected."""
    essid = array.array("B", b"\0" * maxLength["essid"])
    essidPointer, essidLength = essid.buffer_info()
    request = array.array("B",
        bytes(interface.ljust(maxLength["interface"], "\0"), 'ascii') +
        struct.pack("PHH", essidPointer, essidLength, 0)
    )
    fcntl.ioctl(sock.fileno(), calls["SIOCGIWESSID"], request)
    name = str(essid, 'ascii').rstrip("\0")
    if name:
        return name
    return None

class Remotecast(QObject):
    overlayWidthChanged_ = pyqtSignal()
    overlayHeightChanged_ = pyqtSignal()
    def __init__(self):
        QObject.__init__(self)
        self.screenWidth_ = 0
        self.screenHeight_ = 0
        self.overlayWidth_ = 0
        self.overlayHeight_ = 0
        self.overlayWidthChanged_.connect(self.overlayWidthChanged)
        self.overlayHeightChanged_.connect(self.overlayHeightChanged)
        self.wifiEssid_ = 0
        self.wifiSignal_ = -1

    @pyqtProperty(int, notify=overlayWidthChanged_)
    def overlayWidth(self):
        return self.overlayWidth_

    @overlayWidth.setter
    def overlayWidth(self, value):
        self.overlayWidth_ = value

    def overlayWidthChanged(self):
        print("bite width",value)

    @pyqtProperty(int, notify=overlayHeightChanged_)
    def overlayHeight(self):
        return self.overlayHeight_

    @overlayHeight.setter
    def overlayHeight(self, value):
        self.overlayHeight_ = value

    def overlayHeightChanged(self):
        print("bite height",value)

    @pyqtProperty(int)
    def screenWidth(self):
        return self.screenWidth_;

    @screenWidth.setter
    def screenWidth(self, value):
        self.screenWidth_ = value

    @pyqtProperty(int)
    def screenHeight(self):
        return self.screenHeight_;

    @screenHeight.setter
    def screenHeight(self, value):
        self.screenHeight_ = value

    @pyqtSlot()
    def updateWifi(self):
        lines = None
        with open('/proc/net/wireless') as f:
            lines = f.readlines()[2:]
        if not lines:
            self.wifiEssid_ = ""
            self.wifiSignal_ = -1
            return
        ifaces = {}
        for line in lines:
            data = line.split()
            ifaces[data[0]] = data[1:]

        for iface, data in ifaces.items():
            self.wifiEssid_ = getEssid(iface)
            self.wifiSignal_ = int(float(data[1]))

    @pyqtProperty('QString')
    def wifiEssid(self):
        return self.wifiEssid_;

    @pyqtProperty(int)
    def wifiSignal(self):
        return self.wifiSignal_;

    def setGeometry(self, rect):
        self.screenHeight_ = rect.height()
        self.screenWidth_ = rect.width()
        self.overlayHeight_ = self.screenHeight
        self.overlayWidth_ = 250

