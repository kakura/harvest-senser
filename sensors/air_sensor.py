import RPi.GPIO as GPIO
import dht11
import time

GPIO_PIN_NUMBER = 4

class AirSensor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.sensor = dht11.DHT11(pin=GPIO_PIN_NUMBER)

    def setup(self):
        return

    def cleanup(self):
        GPIO.cleanup()

    def measure(self):
        sensor_data = self.sensor.read()

        # 精度の問題で取得した値が 0 になることがあるので何回か再チャレンジする
        try_count = 0
        while sensor_data.temperature == 0 and sensor_data.humidity == 0 and try_count < 10:
            time.sleep(5)
            sensor_data = self.sensor.read()
            try_count += 1

        return {
            "temperature": sensor_data.temperature,
            "humidity": sensor_data.humidity
        }
