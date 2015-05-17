import psutil
import os

from smoverlay.core.monitor import Monitor


class StorageMonitor(Monitor):
    def __init__(self):
        Monitor.__init__(self)
        self.config["mountpoints"] = []
        self.disks = {}
        self.populate()

    def defaultConfig(self):
        skipfs = ["proc", "sysfs", "devtmpfs", "securityfs", "debugfs",
                  "devpts", "cgroup", "pstore", "efivarfs", "configfs",
                  "autofs", "hugetlbfs", "mqueue", "binfmt_misc"]
        skippaths = ('/run', '/sys', '/dev')

        config = Monitor.defaultConfig(self)
        config["mountpoints"] = []
        with open("/proc/mounts") as f:
            for line in f.readlines():
                tokens = line.split()
                if tokens[2] not in skipfs and not tokens[1].startswith(skippaths):
                    config["mountpoints"].append(tokens[1])
        return config

    def update_mountpoint(self, mountpoint, usage, io):
        try:
            write_speed = io.write_bytes / io.write_time
        except Exception:
            write_speed = 0
        try:
            read_speed = io.read_bytes / io.read_time
        except Exception:
            read_speed = 0
        self.disks[mountpoint] = {
            "usage": usage,
            "oldio": io,
            "write": write_speed,
            "read": read_speed
        }

    def getReadSpeed(self, io, oldio, elapsed):
        if not oldio:
            return 0.
        diffbytes = io.read_bytes - oldio.read_bytes
        difftime = io.read_time - oldio.read_time
        if difftime == 0:
            return 0
        return diffbytes / difftime

    def getWriteSpeed(self, io, oldio, elapsed):
        if not oldio:
            return 0.
        diffbytes = io.write_bytes - oldio.write_bytes
        difftime = io.write_time - oldio.write_time
        if difftime == 0:
            return 0
        return diffbytes / difftime

    def update(self, elapsed):
        disksio = psutil.disk_io_counters(perdisk=True)
        partitions = psutil.disk_partitions(all=True) # only mounted: all=True)
        for mountpoint in self.config["mountpoints"]:
            p = [ x for x in partitions if x.mountpoint == mountpoint ]
            if len(p) == 0:
                raise ValueError("Unknown mountpoint %s" % (mountpoint,) )
            p = p[0]
            usage = psutil.disk_usage(mountpoint)
            io = disksio.get(os.path.basename(p.device), None)
            if mountpoint in self.disks:
                oldio = self.disks[mountpoint]["oldio"]
                self.disks[mountpoint] = {
                    "usage": usage,
                    "oldio": io,
                    "write": self.getWriteSpeed(io, oldio, elapsed),
                    "read": self.getReadSpeed(io, oldio, elapsed)
                }
            else:
                self.disks[mountpoint] = {
                    "usage": usage,
                    "oldio": io,
                    "write": 0,
                    "read": 0
                }

            #self.update_mountpoint(mountpoint, usage, io)
        #print("elapsed: %f" % (elapsed,))
        #__import__("pprint").pprint(self.disks)

