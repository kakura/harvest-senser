from sensors.air_sensor import AirSensor
from sensors.ground_sensor import GroundSensor

import time
import socket
import json

INTERVAL = 10 # minutes
SORACOM_ENDPOINT = 'funnel.soracom.io'
SORACOM_PORT     = 23080


def camelize(str):
    return str[0].lower() + str[1:]


class SoracomClient:
    def upload_data(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SORACOM_ENDPOINT, SORACOM_PORT))
            s.sendall(self.build_upload_data(data))
            s.recv(1024)

    def build_upload_data(self, data):
        res_data =  json.dumps(data).encode('utf-8')
        return res_data


class HarvestSensor:
    def __init__(self):
        self.sensors = [
            AirSensor(),
            GroundSensor()
        ]

    def measure(self):
        try:
            # raise Exception('hogeee')
            self.__setup_sensors()
            sensor_data = self.__measure()
        finally:
            self.__cleanup_sensors()

        return sensor_data
    
    def __setup_sensors(self):
        for sensor in self.sensors:
            sensor.setup()

    def __measure(self):
        sensor_data = {}

        for sensor in self.sensors:
            result = sensor.measure()
            sensor_data[camelize(sensor.__class__.__name__)] = result
        
        return sensor_data

    def __cleanup_sensors(self):
        for sensor in self.sensors:
            sensor.cleanup()


if __name__ == "__main__":
    harvest_sensor = HarvestSensor()
    soracom = SoracomClient()

    while True:
        try:
            result = harvest_sensor.measure()
            soracom.upload_data(result)
            print(result)
        except Exception as e:
            print(str(e))
        finally:
            time.sleep(INTERVAL * 60)
 