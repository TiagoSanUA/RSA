import json
import paho.mqtt.client as mqtt
import threading
from time import sleep

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code "+str(rc))
    client.subscribe("vanetza/out/cam")

def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    
    # print('Topic: ' + msg.topic)
    # print('Message' + message)

    obj = json.loads(message)

    if msg.topic=="vanetza/out/cam":
        stationID = obj["stationID"]
        latitude = obj["latitude"]
        longitude = obj["longitude"]
        p = Point([latitude, longitude])
        for key in areas:
            area = areas[key]
            if area.contains(p):
                print("OBU %s is in %s"% (stationID, areas_js[key]["name"]))

    sleep(1)

def generate():
    sleep(1)

with open('areas.json') as f:
    areas_js = json.load(f)

areas = {}
for i in range(0, len(areas_js)):
    areas[i] = Polygon(areas_js[i]["points"])

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.98.20", 1883, 60)

threading.Thread(target=client.loop_forever).start()

while(True):
    generate()
