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

## Run as Service
```bash
sudo cp config/upload_sensor_data.service /etc/systemd/system/upload_sensor_data.service
sudo systemctl enable upload_sensor_data.service
sudo systemctl start upload_sensor_data.service
sudo reboot

sudo systemctl status upload_sensor_data.service
```
