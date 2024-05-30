import json
import paho.mqtt.client as mqtt
import threading
from time import sleep

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

logn = 0

obus = {}

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
            if (not stationID in obus.keys()):
                obus[stationID] = None
            elif (obus[stationID]!=None and not areas[obus[stationID]]["area"].contains(p)):
                print("%d: OBU %s left area %s"% (logn, stationID, obus[stationID]))
                obus[stationID] = None
                logn += 1
            if obus[stationID]==None:
                for key in areas:
                    area = areas[key]["area"]
                    if area.contains(p):
                        if obus[stationID]!=key:
                            print("%d: OBU %s entered area %s"% (logn, stationID, key))
                            obus[stationID] = key
                            logn += 1
                            send_ipfs(stationID)

    sleep(1)

def send_ipfs(stationID):
    ip = "192.168.98." + str(stationID)
    lclient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    lclient.connect(ip, 1883, 60)
    lclient.publish("ipfs", json.dumps(areas[obus[stationID]]["files"]))
    lclient.disconnect()

def generate():
    # f = open('./examples/in_ivim.json')
    # m = json.load(f)
    # ##
    # ##
    # m = json.dumps(m)
    # client.publish("vanetza/in/ivim",m)
    # f.close()
    sleep(1)

with open('areas.json') as f:
    areas_js = json.load(f)

areas = {}
for key in areas_js.keys():
    areas[key] = areas_js[key]
    areas[key]['area'] = Polygon(areas_js[key]["points"])

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.98.10", 1883, 60)

threading.Thread(target=client.loop_forever).start()

while(True):
    generate()
