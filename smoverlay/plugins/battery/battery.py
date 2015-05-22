import os
import re
from smoverlay.core.monitor import Monitor

class BatteryMonitor(Monitor):
    CHARGING = 1
    DISCHARGING = 0

    battery_path = "/sys/class/power_supply/"
    battery_pattern = "BAT%d"

    def __init__(self, battery_id=0):
        Monitor.__init__(self)
        self.status = "Charging"
        self.percent = 0
        self.timeLeft = 0
        self.path = os.path.join(self.battery_path,
                                 self.battery_pattern % self.config["id"])


    def loadConfig(self, config):
        self.config["id"] = config["id"]
        self.path = os.path.join(self.battery_path,
                                 self.battery_pattern % self.config["id"])

    def defaultConfig(self):
        battery_id = 0
        for path, subdirs, files in os.walk(self.battery_path):
            for subdir in subdirs:
                # stop on first match
                m = re.match(r"BAT(\d+)", subdir)
                if m:
                    battery_id = int(m.group(1))
                    break
            break

        cfg = Monitor.defaultConfig(self)
        cfg.update({
            "id": battery_id
        })
        return cfg


    def update(self, elapsed):
        data = {}
        with open(os.path.join(self.path, "uevent")) as f:
            for line in f.readlines():
                (key, value) = line.rstrip().split('=')
                data[key] = value

        self.percent = round(
            int(data["POWER_SUPPLY_CHARGE_NOW"]) /
            int(data["POWER_SUPPLY_CHARGE_FULL_DESIGN"]) * 100
        , 2);

        self.status = data["POWER_SUPPLY_STATUS"]


