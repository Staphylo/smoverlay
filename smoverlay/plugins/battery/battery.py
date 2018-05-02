import os
import re
from smoverlay.core.monitor import Monitor

class Battery(object):
    def __init__(self, uid, path):
        self.uid = uid
        self.path = path
        self.status = "Charging"
        self.percent = 0
        self.percent_dead = 0
        self.percent_ori = 0
        self.timeLeft = 0

    def getCurrentCharge(self, data):
        val = data.get('POWER_SUPPLY_CHARGE_NOW', None)
        if val:
            return int(val)
        return int(data['POWER_SUPPLY_ENERGY_NOW'])

    def getFullCharge(self, data):
        val = data.get('POWER_SUPPLY_CHARGE_FULL', None)
        if val:
            return int(val)
        return int(data['POWER_SUPPLY_ENERGY_FULL'])

    def getFullChargeDesign(self, data):
        val = data.get('POWER_SUPPLY_CHARGE_FULL_DESIGN', None)
        if val:
            return int(val)
        return int(data['POWER_SUPPLY_ENERGY_FULL_DESIGN'])

    def update(self, elapsed):
        data = {}
        with open(os.path.join(self.path, "uevent")) as f:
            for line in f.readlines():
                (key, value) = line.rstrip().split('=')
                data[key] = value

        psc_now = self.getCurrentCharge(data)
        psc_full = self.getFullCharge(data)

        self.percent = round(psc_now / psc_full * 100, 2)
        self.status = data["POWER_SUPPLY_STATUS"]

        # XXX: add red background to show dead battery levels
        psc_full_design = self.getFullChargeDesign(data)
        self.percent_ori = round(psc_now / psc_full_design * 100, 2)
        self.percent_dead = round((psc_full_design - psc_full) /
                psc_full_design * 100, 2)

class BatteryMonitor(Monitor):
    CHARGING = 1
    DISCHARGING = 0

    battery_path = "/sys/class/power_supply/"
    battery_pattern = "BAT%d"

    def __init__(self, battery_id=0):
        Monitor.__init__(self)
        self.batteries = []

    def loadConfig(self, config):
        for uid in config["batteries"]:
            path = os.path.join(self.battery_path,
                                self.battery_pattern % uid)
            self.batteries.append(Battery(uid, path))

    def defaultConfig(self):
        batteries = []
        for entry in os.listdir(self.battery_path):
            m = re.match(r"BAT(\d+)", entry)
            if m:
                batteries.append(int(m.group(1)))
        batteries.sort()

        cfg = Monitor.defaultConfig(self)
        cfg.update({
            "batteries": batteries,
        })
        return cfg

    def update(self, elapsed):
        for battery in self.batteries:
            battery.update(elapsed)


