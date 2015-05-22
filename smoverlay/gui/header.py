import socket
import struct
import array
import fcntl

from smoverlay.gui.qmlobject import QmlObject, qmlProperty, QObject, pyqtSlot

maxLength = {
    "interface": 16,
    "essid": 32
}

# From linux/wireless.h
SIOCGIWESSID = 0x8B1B

# From linux/sockios.h
SIOCETHTOOL = 0x8946

# From linux/if.h
IFF_UP       = 0x1

# From linux/ethtool.h
ETHTOOL_GSET = 0x00000001 # Get settings
ETHTOOL_GLINK = 0x0000000a # Get link status (ethtool_value)

class Header(QmlObject):
    NET_NONE = 0
    NET_ETHERNET = 1
    NET_WIFI = 2

    wifiEssid = qmlProperty('QString')
    wifiSignal = qmlProperty(int)
    ethernetSpeed = qmlProperty(int)
    running = qmlProperty(bool)
    connectionType = qmlProperty(int)

    def __init__(self):
        QObject.__init__(self)
        self.wifiEssid_ = 0
        self.wifiSignal_ = -1
        self.running_ = True
        self.ethiface = b"enp2s0f0"
        self.connectionType = Header.NET_WIFI # FIXME
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketfd = self.socket.fileno()
        self.update()

    def getEssid(self, interface):
        essid = array.array("B", b"\0" * maxLength["essid"])
        essidPointer, essidLength = essid.buffer_info()
        request = array.array("B",
            bytes(interface.ljust(maxLength["interface"], "\0"), 'ascii') +
            struct.pack("PHH", essidPointer, essidLength, 0)
        )
        fcntl.ioctl(self.socketfd, SIOCGIWESSID, request)
        name = str(essid, 'ascii').rstrip("\0")
        if name:
            return name
        return None


    def getLinkInfo(self):
        ecmd = array.array('B', struct.pack('I39s', ETHTOOL_GSET, b'\x00'*39))
        ifreq = struct.pack('16sP', self.ethiface, ecmd.buffer_info()[0])
        try:
            fcntl.ioctl(self.socketfd, SIOCETHTOOL, ifreq)
            res = ecmd.tostring()
            speed, duplex, auto = struct.unpack('12xHB3xB24x', res)
        except IOError:
            speed, duplex, auto = 65535, 255, 255

        # Then get link up/down state
        ecmd = array.array('B', struct.pack('2I', ETHTOOL_GLINK, 0))
        ifreq = struct.pack('16sP', self.ethiface, ecmd.buffer_info()[0])
        fcntl.ioctl(self.socketfd, SIOCETHTOOL, ifreq)
        res = ecmd.tostring()
        up = bool(struct.unpack('4xI', res)[0])

        if speed == 65535:
            speed = 0
        if duplex == 255:
            duplex = None
        else:
            duplex = bool(duplex)
        if auto == 255:
            auto = None
        else:
            auto = bool(auto)
        return speed, duplex, auto, up

    def autodetect(self):
        speed, _, _, up = self.getLinkInfo()
        self.ethernetSpeed = speed
        if up:
            self.connectionType = Header.NET_ETHERNET
        else:
            self.connectionType = Header.NET_WIFI

    @pyqtSlot()
    def update(self):
        # detect connection type
        #self.connectionType = ( self.connectionType + 1 ) % 3
        self.autodetect()
        if self.connectionType & Header.NET_ETHERNET:
            pass
        if self.connectionType & Header.NET_WIFI:
            lines = None
            with open('/proc/net/wireless') as f:
                lines = f.readlines()[2:]
            if not lines:
                self.wifiEssid = ""
                self.wifiSignal = -1
                self.connectionType = Header.NET_NONE
                return
            ifaces = {}
            for line in lines:
                data = line.split()
                ifaces[data[0]] = data[1:]

            for iface, data in ifaces.items():
                self.wifiEssid = self.getEssid(iface)
                self.wifiSignal = int(float(data[1]))


