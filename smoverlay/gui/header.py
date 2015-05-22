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
        self.connectionType = Header.NET_WIFI # FIXME
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketfd = self.socket.fileno()
        # TODO use configuration for the interfaces by default
        ethifaces = self.getEthernetIfaces()
        self.ethiface = ethifaces[0] if ethifaces else None
        wlifaces = self.getWirelessIfaces()
        self.wliface = wlifaces[0] if wlifaces else None
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

    def getIfaces(self, prefix):
        interfaces = []
        with open("/proc/net/dev", "r") as f:
            for line in f.readlines()[2:]:
                data = line.rstrip().split()
                ifname = data[0][:-1]
                if ifname.startswith(prefix):
                    interfaces.append(ifname)
        return interfaces

    def getEthernetIfaces(self):
        return self.getIfaces(("en", "et"))

    def getLinkInfo(self):
        iface = bytes(self.ethiface, 'ascii')
        ecmd = array.array('B', struct.pack('2I', ETHTOOL_GLINK, 0))
        ifreq = struct.pack('16sP', iface, ecmd.buffer_info()[0])
        fcntl.ioctl(self.socketfd, SIOCETHTOOL, ifreq)
        res = ecmd.tostring()
        up = bool(struct.unpack('4xI', res)[0])
        if not up:
            return None, None, None, False

        ecmd = array.array('B', struct.pack('I39s', ETHTOOL_GSET, b'\x00'*39))
        ifreq = struct.pack('16sP', iface, ecmd.buffer_info()[0])
        try:
            fcntl.ioctl(self.socketfd, SIOCETHTOOL, ifreq)
            res = ecmd.tostring()
            speed, duplex, auto = struct.unpack('12xHB3xB24x', res)
        except IOError:
            speed, duplex, auto = 65535, 255, 255

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

    def getWirelessIfaces(self):
        return self.getIfaces('wl')

    def getWirelessInfo(self):
        lines = None
        with open('/proc/net/wireless') as f:
            for line in f.readlines()[2:]:
                data = line.split()
                ifname = data[0][:-1]
                if ifname != self.wliface:
                    continue
                essid = self.getEssid(ifname)
                signal = int(float(data[2]))
                return signal, essid

        return None, None

    def autodetect(self):
        if self.ethiface:
            speed, _, _, up = self.getLinkInfo()
            if up:
                self.ethernetSpeed = speed
                return Header.NET_ETHERNET

        if self.wliface:
            signal, essid = self.getWirelessInfo()
            if signal:
                self.wifiSignal = signal
                self.wifiEssid = essid
                return Header.NET_WIFI

        return Header.NET_NONE

    @pyqtSlot()
    def update(self):
        self.connectionType = self.autodetect()


