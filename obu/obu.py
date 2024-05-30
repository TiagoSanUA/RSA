import os
import json
import paho.mqtt.client as mqtt
import threading
from time import sleep

import requests

stationID = 12
stationType = 5
latitude = 40.634200
longitude = -8.659871
moving = False
target_latitude = 40.634200
target_longitude = -8.659871

kmh = 40
kms = 40/3600
speed = kms/111

def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code "+str(rc))
    client.subscribe("vanetza/out/cam")
    client.subscribe("commands/teleport")
    client.subscribe("commands/move")
    client.subscribe("ipfs")

def on_message(client, userdata, msg):
    global latitude
    global longitude
    global moving
    global target_latitude
    global target_longitude

    message = msg.payload.decode('utf-8')
    
    # print('Topic: ' + msg.topic)
    # print('Message' + message)

    obj = json.loads(message)

    if msg.topic=="commands/move":
        target_latitude = float(obj["latitude"])
        target_longitude = float(obj["longitude"])
        moving = True
        print("Moving to: %f, %f"%(target_latitude,target_longitude))

    if msg.topic=="commands/teleport":
        latitude = float(obj["latitude"])
        longitude = float(obj["longitude"])
        moving = False
        target_latitude = latitude
        target_longitude = longitude
        print("Teleporting to: %f, %f"%(target_latitude,target_longitude))
    
    if msg.topic=="ipfs":
        print("Received ipfs file information: %s"%(obj))
        for file in obj:
            print("Downloading %s"%file["hash"])
            x = requests.get('http://192.168.98.13:8080/ipfs/%s'%(file["hash"]))
            print(x.text)
            print("Download complete")

    sleep(1)

def generate():
    global latitude
    global longitude
    global moving
    global target_latitude
    global target_longitude

    f = open('../examples/in_cam.json')
    m = json.load(f)
    ##
    m["stationID"] = stationID
    m["stationType"] = stationType

    if (moving):
        difference_lat = target_latitude - latitude
        difference_lon = target_longitude - longitude
        if difference_lat>0:
            if difference_lat<speed:
                latitude += difference_lat
            else:
                latitude += speed
        elif difference_lat<0:
            if difference_lat>-speed:
                latitude += difference_lat
            else:
                latitude -= speed
        if difference_lon>0:
            if difference_lon<speed:
                longitude += difference_lon
            else:
                longitude += speed
        elif difference_lon<0:
            if difference_lon>-speed:
                longitude += difference_lon
            else:
                longitude -= speed
        if difference_lat==0 and difference_lon==0:
            moving = False
    
    m["latitude"] = latitude
    m["longitude"] = longitude
    ##
    m = json.dumps(m)
    client.publish("vanetza/in/cam",m)
    f.close()
    sleep(1)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.98.12", 1883, 60)

threading.Thread(target=client.loop_forever).start()

while(True):
    generate()
