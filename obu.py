import os
import json
import paho.mqtt.client as mqtt
import threading
from time import sleep

def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code "+str(rc))
    client.subscribe("vanetza/out/cam")

def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    
    print('Topic: ' + msg.topic)
    print('Message' + message)

    obj = json.loads(message)

    sleep(1)

def generate():
    f = open('examples/in_cam.json')
    m = json.load(f)
    ##
    m['latitude'] = os.environ['LATITUDE']
    m['longitude'] = os.environ['LONGITUDE']
    ##
    m = json.dumps(m)
    client.publish("vanetza/in/cam",m)
    f.close()
    sleep(1)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.98.10", 1883, 60)

threading.Thread(target=client.loop_forever).start()

while(True):
    generate()
