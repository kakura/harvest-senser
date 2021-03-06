import serial
import time
import pprint
import json

PRODUCT_NUMBER = 2 # 5WT
SENSOR_COUNT   = 1
WAIT_TIME      = 0.5

class GroundSensor:
    def __init__(self, port_name):
        self.address_type_list = []
        self.port_name = port_name
    
    def power_on(self):
        self.sdi.setRTS(True)
        time.sleep(0.05)

    def cleanup(self):
        try:
            self.sdi
        except AttributeError:
            return
        else:
            self.sdi.close()
            self.sdi.setRTS(False)

    def setup(self):
        try_count = 0
        while try_count < 10:
            try:
                self.sdi = serial.Serial(
                    port = self.port_name,
                    baudrate = 1200,
                    bytesize = serial.SEVENBITS,
                    parity = serial.PARITY_EVEN,
                    stopbits = serial.STOPBITS_ONE,
                    timeout = 0,
                    write_timeout = 0)
                break
            except Exception as e:
                print(str(e))
                try_count += 1
                time.sleep(10)

        self.power_on()
        self.__cleanup()
        if len(self.address_type_list) == 0:
            self.__scan_device()

    def measure(self):
        mesured_data = []
        for address_type in self.address_type_list:
            address = address_type[0]
            type = address_type[1]

            self.__cleanup()
            self.__break_send(0.02)
            request = str(address) + "M!"
            self.sdi.write( request.encode() )
            time.sleep(WAIT_TIME)
            #Write Check
            response = self.sdi.readline()
            response = response.rstrip()            # 改行文字削除
            # <BR>0M!00013<CR><LF>
            resAddress = response[4:5].decode('Shift_JIS')
            resInterval = response[5:8].decode('Shift_JIS')
            resItemCount = response[8:9].decode('Shift_JIS')
            if str(address) != resAddress:
                print("Request failed:Address error.")
                return
            if str(type) != resItemCount:
                print("Request failed:Item Count is different.")
                return
            time.sleep(int(resInterval))

            self.__cleanup()
            self.__break_send(0.02)
            request = str(address) + "D0!"
            self.sdi.write(request.encode())
            time.sleep(WAIT_TIME)
            measured = self.sdi.readline()
            # <BR>0D0!0
            if measured[1:6].decode('Shift_JIS') == str(address) + "D0!"+ str(address):
                measured = measured.rstrip().decode('Shift_JIS')            # 改行文字削除
                replaced = measured.replace('+',',')
                replaced = replaced.replace('-',',-')
                data = replaced.split(',')
                mesured_data.append(self.__build_response_data(data))
            else:
                print("Response invalid")
        return mesured_data

    def __cleanup(self):
        self.sdi.reset_input_buffer()
        self.sdi.reset_output_buffer()

    def __break_send(self, interval):
        self.sdi.sendBreak(interval)
        time.sleep(interval)

    def __build_response_data(self, data):
        return { 
            "waterContent": float(data[1]),
            "temperature": float(data[2])
        }

    def __scan_device(self):
        address=0
        while address < SENSOR_COUNT:
            self.__cleanup()
            self.__break_send(0.02)

            request = str(address) + "I!"

            self.sdi.write(request.encode())

            time.sleep(WAIT_TIME)
            #Write Check
            response = self.sdi.readline()
            #Parse
            length = len(response)
            if length == 34:
                sdi_ver = response[5:7].decode('Shift_JIS')
                company = response[7:15].decode('Shift_JIS').strip()
                product = response[15:21].decode('Shift_JIS').strip()
                version = response[21:24].decode('Shift_JIS')
                option  = response[24:length-2].decode('Shift_JIS').strip()
                if response[4:5].decode('Shift_JIS') != str(address):
                    address = address + 1
                    continue
                if sdi_ver != "13":
                    address = address + 1
                    continue
                self.address_type_list.append([address, PRODUCT_NUMBER])
            address = address + 1
