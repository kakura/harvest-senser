import mh_z19

class AirSensor:
    def setup(self):
        return

    def cleanup(self):
        return

    def measure(self):
        data = mh_z19.read(serial_console_untouched=True)
        return data
