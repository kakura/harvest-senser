# Harvest Sensor

## Load sensors configuration
```bash
sudo cp config/rc.local /etc/rc.local
sudo reboot
```

## Setup application
```bash
sudo apt-get update
sudo apt install python3-pip
sudo pip3 install -r requirements.txt
```

```
cp .env.template .env # and fill values
```

## Start monitoring
```
python3 harvest_sensor.py
```

and you can get values like below
```json
{
    "thermoSensor": {
        "temperature": 28.1,
        "humidity": 59.0
    }, 
    "groundSensor": [
        {
            "waterContent": 21.6,
            "temperature": 26.0
        }
    ]
}
```

## Run as a service
```bash
sudo cp config/upload_sensor_data.service /etc/systemd/system/upload_sensor_data.service
sudo systemctl enable upload_sensor_data.service
sudo systemctl start upload_sensor_data.service
sudo reboot

sudo systemctl status upload_sensor_data.service
```
