import sys
import os # to fix SSL cert
from Adafruit_IO import MQTTClient

# os.environ['REQUESTS_CA_BUNDLE'] = '/usr/local/etc/openssl@1.1/cert.pem'
os.environ['SSL_CERT_FILE'] = '/etc/ssl/cert.pem'

import ssl
print(ssl.get_default_verify_paths())

AIO_FEED_ID = "sensor1"
AIO_USERNAME = "phucnguyenng"
AIO_KEY = "aio_paYN09wK5fmBNFRru9LEiNBO0png"


def connected(client):
    print("Connected successfully!")
    client.subscribe(AIO_FEED_ID)

def subscribe(client , userdata , mid , granted_qos):
    print("Subcribed successfully")

def disconnected(client):
    print("Disconnecting...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Received: " + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

while True:
    pass