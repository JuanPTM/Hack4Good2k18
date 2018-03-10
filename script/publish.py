import paho.mqtt.client as mqtt
import time
#client  = Client(, clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)


client =mqtt.Client(client_id="pulsera_abuelo")
client.connect("158.49.112.108", port=8080)

while True:
  client.publish("GsmClient/2/posi","00.00,15.248")
  time.sleep(5)
