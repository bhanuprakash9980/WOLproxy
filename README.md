# Raspberry Pi as Wake on LAN proxy

## Introduction

A script for making Raspberrypi as a proxy for wake on lan. Uses adafruit as MQTT broker, Pi as MQTT client which sends magic packet to device in network on receiving "1" from the feed subscribed.

This will allow you to turn your device fom internet without port forwarding.
Further you can integrate this with IFTTT and ai assistants like Google Assistant to turn the device on with voice commands.

run this script as a daemon in your pi. I personally use systemd for this purpose.

```service
[Unit]
Description=Wake on Lan Forwarder service
After=multi-user.target

[Service]
Type=idle
Restart=on-failure
ExecStart=<absoltute path to python3 binary> <absolute path to main.py>

[Install]
WantedBy=multi-user.target
```

## Configuration

Fill the following details in [config.ini](./config.ini) file:

- MAC address of the device to be turned on. (Don't forget to enable WakeonLan in bios and macaddress can be found with `ifconfig`)
- IO key from adafruit
- IO username from adafruit
  ![io_key](https://nc.bhanuprakash.tech/s/gYCBRFna42dHBtz/download/screenshot-io.png)
- Feed name from adafruit
  ![feed](https://nc.bhanuprakash.tech/s/WqwiBTZ8CAka66q/download/screenshot-io%20%282%29.png)

## Usage

`pip3 install -r requirements.txt`

`python3 main.py`
