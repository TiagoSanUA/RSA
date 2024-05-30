import json
import paho.mqtt.client as mqtt
import threading
import ipfsapi

from time import sleep

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

logn = 0

def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code "+str(rc))
    client.subscribe("vanetza/out/cam")

def on_message(client, userdata, msg):
    global logn

    message = msg.payload.decode('utf-8')
    
    # print('Topic: ' + msg.topic)
    # print('Message' + message)

    obj = json.loads(message)

    if msg.topic=="vanetza/out/cam":
        stationID = obj["stationID"]
        stationType = obj["stationType"]
        latitude = obj["latitude"]
        longitude = obj["longitude"]
        if (stationType==5):
            p = Point([latitude, longitude])
            for key in areas:
                area = areas[key]
                if area.contains(p):
                    print("%d: OBU %s is in %s"% (logn, stationID, areas_js[key]["name"]))
                    logn += 1
                    # # Add the file to IPFS
                    # try:
                    #     res = ipfs_api.add('data/obu.jpg')
                    #     file_hash = res['Hash']
                    #     print(f'File added to IPFS with hash: {file_hash}')

                    #     # Publish the file hash over MQTT
                    #     client.publish("vanetza/out/ipfs", json.dumps({"stationID": stationID, "file_hash": file_hash}))

                    # except Exception as e:
                    #     print(f'An error occurred while adding file to IPFS: {e}')



    sleep(1)

def generate():
    sleep(1)

with open('areas.json') as f:
    areas_js = json.load(f)

areas = {}
for i in range(0, len(areas_js)):
    areas[i] = Polygon(areas_js[i]["points"])

#ipfs_api = ipfsapi.connect('0.0.0.0', 5001)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.98.10", 1883, 60)

threading.Thread(target=client.loop_forever).start()

while(True):
    generate()
