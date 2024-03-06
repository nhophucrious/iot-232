import sys
import os # to fix SSL cert
from Adafruit_IO import MQTTClient
from dotenv import load_dotenv
# import ssl

import time
import random

# os.environ['REQUESTS_CA_BUNDLE'] = '/usr/local/etc/openssl@1.1/cert.pem'
os.environ['SSL_CERT_FILE'] = '/etc/ssl/cert.pem'

# print(ssl.get_default_verify_paths())

AIO_FEED_IDS = [
    "button1",
    "button2",
]

AIO_USERNAME = ""
AIO_KEY = ""

# read from .env
load_dotenv()
AIO_USERNAME = os.getenv("AIO_USERNAME")
AIO_KEY = os.getenv("AIO_KEY")
print(AIO_USERNAME, AIO_KEY)


def connected(client):
    print("Connected successfully!")
    for AIO_FEED_ID in AIO_FEED_IDS:
        client.subscribe(AIO_FEED_ID)

def subscribe(client , userdata , mid , granted_qos):
    print("Subcribed successfully")

def disconnected(client):
    print("Disconnecting...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Received: " + payload + " from " + feed_id)

try:
    client = MQTTClient(AIO_USERNAME, AIO_KEY)
except Exception as e:
    print("Some shit happened: ", e)

client.on_connect = connected # assign call-back to object
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background() # loop foreground blocks everything...

counter = 10
my_type = 0
while True:
    counter -= 1
    if counter <= 0:
        counter = 10

        print("publishing random stuff")
        if my_type == 0:
            print("sending temperature data...")
            temperature = random.randint(10, 40)
            client.publish("sensor1", temperature)
            my_type = 1
        elif my_type == 1:
            print("sending light data...")
            light = random.randint(100, 500)
            client.publish("sensor2", light)
            my_type = 2
        else:
            print("sending humidity data...")
            humidity = random.randint(60, 100)
            client.publish("sensor3", humidity)
            my_type = 0
    # sleep for one second
    time.sleep(1) 
    pass