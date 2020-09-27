from sensors.thermo_sensor import ThermoSensor
from sensors.ground_sensor import GroundSensor
from sensors.air_sensor import AirSensor

import os
import time
import datetime
import socket
import json
import slackweb
from dotenv import load_dotenv
import sys, traceback

SORACOM_ENDPOINT = 'funnel.soracom.io'
SORACOM_PORT     = 23080


def camelize(str):
    return str[0].lower() + str[1:]


class SoracomClient:
    def upload_data(self, data):
        max_try_count = 10
        try_count = 0
        while try_count < max_try_count:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((SORACOM_ENDPOINT, SORACOM_PORT))
                    s.sendall(self.build_upload_data(data))
                    s.recv(1024)
                break
            except Exception as e:
                print(e)
                if try_count >= max_try_count:
                    raise Exception(e)
                time.sleep(10)
                try_count += 1

    def build_upload_data(self, data):
        res_data =  json.dumps(data).encode('utf-8')
        return res_data


class HarvestSensor:
    def __init__(self):
        self.sensors = [
            ThermoSensor(gpio_pin_number=4),
            GroundSensor(port_name='/dev/ttyUSB4'),
            AirSensor()
        ]

    def measure(self):
        try:
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

            # 土壌センサーは複数接続されることが想定されているため、配列で値が返ってくるようになっていますが、
            # 当分はひとつしか使わない想定なのでひとつ目を取り出して使います
            if sensor.__class__.__name__ == 'GroundSensor':
              result = result[0]

            sensor_data[camelize(sensor.__class__.__name__)] = result
        
        return sensor_data

    def __cleanup_sensors(self):
        for sensor in self.sensors:
            sensor.cleanup()


if __name__ == "__main__":
    try:
        load_dotenv()
        slack = slackweb.Slack(url=os.environ['SLACK_URL'])

        harvest_sensor = HarvestSensor()
        soracom = SoracomClient()

        result = harvest_sensor.measure()
        soracom.upload_data(result)

        print(result)
    except KeyboardInterrupt:
        print('keyboard interrupted')
        sys.exit()
    except:
        msg = f"```\n{traceback.format_exc()}```"
        print(datetime.datetime.now(), msg, file=sys.stderr)
        slack.notify(text=msg)