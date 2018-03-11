#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import paho.mqtt.client as mqtt
import hashlib

value = sys.argv[1]

client =mqtt.Client(client_id="pulsera_abuelo")
client.connect("avisos", port=1883)

id_digest = hashlib.sha256(str(value).encode('utf-8')).hexdigest()

client.publish("dbNotification",id_digest)

