#!/usr/bin/python
import configparser
from datetime import datetime

# Imported send_magic_packet for broadcasting magic packet
from wakeonlan import send_magic_packet

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient


config = configparser.ConfigParser()
config.read("./config.ini")

# device mac-address to which you want to send magic packet
MAC_ADDRESS = config["WOL"]["MAC_ADDRESS"]

ADAFRUIT_IO_KEY = config["ADAFRUIT"]["IO_KEY"]
ADAFRUIT_IO_USERNAME = config["ADAFRUIT"]["IO_USERNAME"]
ADAFRUIT_FEED_NAME = config["ADAFRUIT"]["FEED_NAME"]

# Define callback functions which will be called when certain events happen.


def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    with open("./wol.log", "a") as f:
        print(
            f"{datetime.now()} INFO Connected to Adafruit IO!  Listening for {ADAFRUIT_FEED_NAME} changes...",
            file=f,
        )
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe(ADAFRUIT_FEED_NAME)


def subscribe(client, userdata, mid, granted_qos):
    # This method is called when the client subscribes to a new feed.
    with open("./wol.log", "a") as f:
        print(
            f"{datetime.now()} INFO Subscribed to {ADAFRUIT_FEED_NAME} with QoS {granted_qos[0]}",
            file=f,
        )


def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    with open("./wol.log", "a") as f:
        print(f"{datetime.now()} WARNING Disconnected from Adafruit IO!", file=f)


def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    if payload == "1":
        send_magic_packet(MAC_ADDRESS)
    with open("./wol.log", "a") as f:
        print(
            f"{datetime.now()} INFO Feed {feed_id} received new value: {payload}",
            file=f,
        )
        print(f"{datetime.now()} INFO Computer is ON!!", file=f)


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

# Connect to the Adafruit IO server.
client.connect()

# Start a message loop that blocks forever waiting for MQTT messages to be
# received.  Note there are other options for running the event loop like doing
# so in a background thread--see the mqtt_client.py example to learn more.
client.loop_blocking()
