import os
from smoverlay.core.monitor import Monitor

class BatteryMonitor(Monitor):
    CHARGING = 1
    DISCHARGING = 0

    battery_path = "/sys/class/power_supply/"
    battery_pattern = "BAT%d"

    def __init__(self, battery_id=0):
        Monitor.__init__(self)
        self.battery_folder = os.path.join(self.battery_path,
                                           self.battery_pattern % battery_id)

        self.status = "Charging"
        self.percent = 0
        self.timeLeft = 0


    def update(self, elapsed):
        data = {}
        with open(os.path.join(self.battery_folder, "uevent")) as f:
            for line in f.readlines():
                (key, value) = line.rstrip().split('=')
                data[key] = value

        self.percent = round(
            int(data["POWER_SUPPLY_CHARGE_NOW"]) /
            int(data["POWER_SUPPLY_CHARGE_FULL_DESIGN"]) * 100
        , 2);

        self.status = data["POWER_SUPPLY_STATUS"]


