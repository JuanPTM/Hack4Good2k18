#!/usr/bin/python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt

tipoAvisos = ["Alert", "Battery", "Broken", "AlternativeRoute"]
broker_address = "192.168.0.161"
broker_port = 1883


clientPos = mqtt.Client("ProxyServerPOS")  # create new instance
clientBat = mqtt.Client("ProxyServerBAT")  # create new instance
clientBroken = mqtt.Client("ProxyServerBROKEN")  # create new instance
clientAvi = mqtt.Client("ProxyServerAVISOS")  # create new instance
clientDB = mqtt.Client("ProxyServerDB")  # create new instance
clients = [clientPos,clientBat,clientBroken,clientAvi,clientDB]

# CALLBACK POSITION
def subs_pos_handler(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    topic_id = message.topic.split("/")[0]
    pos = msg.split(",")
    pos = map(float, pos)
    # TODO PYMOOOOOOONGO
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
    elif bat > 50:
        clientAvi.publish(topic_id + "/ad", tipoAvisos[1] + "," + "75")
    elif bat > 25:
        clientAvi.publish(topic_id + "/ad", tipoAvisos[1] + "," + "50")
    elif bat < 25.:
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
    if broken is 1:
        clientAvi.publish(topic_id + "/ad", tipoAvisos[3] + "," + "SE HA ROTO LA PULSERA")
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("\n")

# CALLBACK DATABASE
def subs_db_handler(client,userdata,message):
    msg = str(message.payload.decode("utf-8"))
    topic_id = message.topic.split("/")[0]
    dev_id = msg.split(",")
    clientPos.subscribe(dev_id[0]+"/pos")
    clientBroken.subscribe(dev_id[0] + "/bat")
    clientBat.subscribe(dev_id[0] + "/brok")
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("\n")



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