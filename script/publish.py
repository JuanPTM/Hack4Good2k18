#!/usr/bin/python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import random as rn
#client  = Client(, clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)
points = [(39.479129, -6.342678),(39.479288, -6.342722),(39.479481, -6.342877),(39.478930, -6.343002),(39.478407, -6.342376),(39.479305, -6.342317),(39.479679, -6.342869),(39.479699, -6.341873)]
bat = [100.,80.,98.,67.,45.,25.,15.,9.]
broken = [0,0,0,0,0,1,1,0]
client =mqtt.Client(client_id="pulsera_abuelo")
client.connect("192.168.0.161", port=1883)

id = "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b"

client.publish("dbNotification",id)

for i in range(len(points)):
    client.publish(id+"/pos",str(points[i][0])+","+str(points[i][1]))
    client.publish(id+"/bat",str(bat[i]))
    client.publish(id+"/brok",str(broken[i]))

    time.sleep(5)
