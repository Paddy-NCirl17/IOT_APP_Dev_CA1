# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.client as mqtt
from grovepi import *
import grovepi
import time
import json
from threading import Thread
from time import gmtime, strftime
from datetime import datetime

############# Port Selection#######
dht_sensor_port = 7
dht_sensor_type = 0
ultrasonic_ranger = 2

broker_url = "broker.mqttdashboard.com"
broker_port = 1883
client = mqtt.Client("PADDY-IOT2")
client.connect(broker_url, broker_port)

def temperature():
	[ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)
	return temp
def ranger():
	light = grovepi.ultrasonicRead(ultrasonic_ranger)
	return "Light On"

while True:
	try:
		sensors={"temp":temperature(), "door":ranger(), "timestamp": datetime.now().isoformat()}
		client.publish(topic="PJM1/sensor", payload=json.dumps(sensors), qos=1, retain=False)			
		print("publishing")
		time.sleep(1)
	except KeyboardInterrupt:
		print("User Interrupt")
		break
	except IOError:
		print ("Error") 