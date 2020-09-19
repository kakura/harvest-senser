from sensors.air_sensor import AirSensor
from sensors.ground_sensor import GroundSensor

import time

INTERVAL = 0.1 # minutes

class HarvestSensor:
    def __init__(self):
        self.sensors = [
            AirSensor(),
            GroundSensor()
        ]

    def measure(self):
        self.__setup_sensors()
        self.__measure()
        self.__cleanup_sensors()
    
    def __setup_sensors(self):
        for sensor in self.sensors:
            sensor.setup()

    def __measure(self):
        for sensor in self.sensors:
            result = sensor.measure()
            print(result)

    def __cleanup_sensors(self):
        for sensor in self.sensors:
            sensor.cleanup()


if __name__ == "__main__":
    harvest_sensor = HarvestSensor()

    while True:
        harvest_sensor.measure()
        time.sleep(INTERVAL * 60)
