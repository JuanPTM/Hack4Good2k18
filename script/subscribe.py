import paho.mqtt.client as mqtt #import the client1
import time
############
def on_message(client, userdata, message):
	print("message received " ,str(message.payload.decode("utf-8")))
	print("message topic=",message.topic)
	print("message qos=",message.qos)
	print("message retain flag=",message.retain)
########################################
broker_address="158.49.112.108"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("Subs") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address,port=8080) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic","GsmClient/2/posi")
client.subscribe("GsmClient/2/posi")
time.sleep(120) # wait
client.loop_stop() #stop the loop