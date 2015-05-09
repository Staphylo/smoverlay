import psutil

from smoverlay.core.monitor import Monitor

class NetworkMonitor(Monitor):
    def __init__(self):
        Monitor.__init__(self)
        self.interfaces = {}
        self.populate()

    def update(self, elapsed):
        interfaces = {}
        with open("/proc/net/dev", "r") as f:
            for line in f.readlines()[2:]:
                data = line.rstrip().split()
                ifname = data[0][:-1]
                rxbytes = int(data[1])
                txbytes = int(data[9])
                if ifname in self.interfaces:
                    info = self.interfaces[ifname]
                    rxspeed = round((rxbytes - info["rxlast"]) / elapsed)
                    txspeed = round((txbytes - info["txlast"]) / elapsed)
                    rxhistory = info["rxspeedhistory"] + [rxspeed]
                    txhistory = info["txspeedhistory"] + [txspeed]
                    info["rxspeed"] = sum(rxhistory) / len(rxhistory)
                    info["txspeed"] = sum(txhistory) / len(txhistory)
                    info["rxspeedhistory"] = rxhistory[-4:]
                    info["txspeedhistory"] = txhistory[-4:]
                    info["rxlast"] = rxbytes
                    info["txlast"] = txbytes
                    #print("update",elapsed,ifname,info)
                else:
                    #print("add %s" % ifname)
                    self.interfaces[ifname] = {
                        "rxspeedhistory": [],
                        "txspeedhistory": [],
                        "rxspeed": 0,
                        "txspeed": 0,
                        "rxlast": rxbytes,
                        "txlast": txbytes
                    }

