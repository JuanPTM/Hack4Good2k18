#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import requests
import paho.mqtt.client as mqtt
import yaml
import socket

with open("config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

cfgMqtt = cfg['mqtt'] 
cfgApi = cfg['api']


tipoAvisos = ["Alert", "Battery", "Broken", "AlternativeRoute"]
broker_address = socket.gethostbyname(cfgMqtt['hostname'])
broker_port = int(cfgMqtt['port'])

url_api = "http://{}".format(socket.gethostbyname(cfgApi['hostname']))
api_port = int(cfgApi['port'])
headers = {'Content-Type': 'application/json'}

print(broker_address,url_api)

clientPos = mqtt.Client("TProxyServerPOS")  # create new instance
clientBat = mqtt.Client("TProxyServerBAT")  # create new instance
clientBroken = mqtt.Client("TProxyServerBROKEN")  # create new instance
clientAvi = mqtt.Client("TProxyServerAVISOS")  # create new instance
clientDB = mqtt.Client("TProxyServerDB")  # create new instance
clients = [clientPos,clientBat,clientBroken,clientAvi,clientDB]

# CALLBACK POSITION
def subs_pos_handler(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    topic_id = message.topic.split("/")[0]
    pos = msg.split(",")
    pos = list(map(float, pos))

    num_fences = checkfence(topic_id,pos[0],pos[1])
    if num_fences == 0:
        clientAvi.publish(topic_id + "/ad", tipoAvisos[0] + "," + "Se va.")
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("\n")


# CALLBACK BATTERY
def subs_bat_handler(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    topic_id = message.topic.split("/")[0]
    bat = msg.split(",")
    bat = float(bat[0])
    if bat > 75.:
        clientAvi.publish(topic_id + "/ad", tipoAvisos[1] + "," + "100")
    elif bat > 50.:
        clientAvi.publish(topic_id + "/ad", tipoAvisos[1] + "," + "75")
    elif bat > 25.:
        clientAvi.publish(topic_id + "/ad", tipoAvisos[1] + "," + "50")
    elif bat <= 25.:
        clientAvi.publish(topic_id + "/ad", tipoAvisos[1] + "," + "25")
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("\n")

# CALLBACK BROKEN
def subs_broken_handler(client,userdata,message):
    msg = str(message.payload.decode("utf-8"))
    topic_id = message.topic.split("/")[0]
    broken = msg.split(",")
    broken = int(broken[0]);
    if broken == 1:
        clientAvi.publish(topic_id + "/ad", tipoAvisos[2] + "," + "SE HA ROTO LA PULSERA")
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("\n")

# CALLBACK DATABASE
def subs_db_handler(client,userdata,message):
    msg = str(message.payload.decode("utf-8"))
    topic_id = message.topic.split("/")[0]
    dev_id = msg.split(",")
    print(dev_id)
    if str(dev_id[1]) == "up":
        clientPos.subscribe(dev_id[0]+"/pos")
        clientBroken.subscribe(dev_id[0] + "/brok")
        clientBat.subscribe(dev_id[0] + "/bat")
    elif dev_id[1] == "down":
        clientPos.unsubscribe(dev_id[0]+"/pos")
        clientBroken.unsubscribe(dev_id[0] + "/brok")
        clientBat.unsubscribe(dev_id[0] + "/bat")
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("\n")

def checkfence(device_id,lat,lon):
    api_url = '{0}:{2}/checkfence/{1}'.format(url_api,device_id,api_port)
 #   print(api_url)
    params= {'lat':lat,'lon':lon}
    params = json.dumps(params).encode('utf8')
    response = requests.post(api_url,data=params, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None



clientPos.on_message = subs_pos_handler  # attach function to callback
clientBat.on_message = subs_bat_handler  # attach function to callback
clientBroken.on_message = subs_broken_handler  # attach function to callback
clientDB.on_message = subs_db_handler  # attach function to callback

for clt in clients:
    clt.connect(broker_address, port=broker_port)  # connect to broker
    clt.loop_start()  # start the loop
clientDB.subscribe("dbNotification")
while True:
    pass
