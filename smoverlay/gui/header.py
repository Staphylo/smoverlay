import socket
import struct
import array
import fcntl

from smoverlay.gui.qmlobject import QmlObject, qmlProperty, QObject, pyqtSlot

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

class Header(QmlObject):
    wifiEssid = qmlProperty('QString')
    wifiSignal = qmlProperty(int)

    def __init__(self):
        QObject.__init__(self)
        self.wifiEssid_ = 0
        self.wifiSignal_ = -1
        self.updateWifi()

    @pyqtSlot()
    def updateWifi(self):
        lines = None
        with open('/proc/net/wireless') as f:
            lines = f.readlines()[2:]
        if not lines:
            self.wifiEssid = ""
            self.wifiSignal = -1
            return
        ifaces = {}
        for line in lines:
            data = line.split()
            ifaces[data[0]] = data[1:]

        for iface, data in ifaces.items():
            self.wifiEssid = getEssid(iface)
            self.wifiSignal = int(float(data[1]))


