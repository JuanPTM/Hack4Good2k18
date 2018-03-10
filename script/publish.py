import paho.mqtt.client as mqtt
import time
import random as rn
#client  = Client(, clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)
points = [(39.479129, -6.342678),(39.479288, -6.342722),(39.479481, -6.342877),(39.478930, -6.343002),(39.478407, -6.342376),(39.479305, -6.342317),(39.479679, -6.342869),(39.479699, -6.341873)]

client =mqtt.Client(client_id="pulsera_abuelo")
client.connect("158.49.112.108", port=8080)

for point in points:
	client.publish("GsmClient/2/posi",str(point[0])+","+str(point[1]))
	time.sleep(5)
