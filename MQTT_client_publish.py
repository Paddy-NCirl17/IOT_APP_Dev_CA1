
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import json
from threading import Thread
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)#fan
GPIO.setup(23,GPIO.OUT)#led

 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc): 
    if rc == 0:
        print("Connected to broker: "+ broker_address) 
        global Connected                #Use global variable
        Connected = True                #Signal connection  
    else: 
        print("Connection failed")
 
def on_message(client, userdata, message):
    print("message received " ,message.payload.decode("utf-8","ignore"))
    print("message topic=",message.topic)
    sensors = json.loads(message.payload.decode("utf-8","ignore"))
    temp = (sensors["temp"])
    light = (sensors["door"])
    print(temp)
    print(light)
    
    if message.topic =="PJM1/sensor" and temp > 3:        
        GPIO.output(18,GPIO.HIGH)         
    else:
        GPIO.output(18,GPIO.LOW)
                
    if message.topic =="PJM1/sensor" and light > 3:
        GPIO.output(23,GPIO.HIGH)
    else:
        GPIO.output(23,GPIO.LOW)           
 
# MQTT client.
Connected = False
broker_address="broker.mqttdashboard.com"
client = mqtt.Client("PADDY-IOT")
client.on_connect = on_connect
client.on_message = on_message 
client.connect(broker_address)

client.loop_start()

publisher_state=False
def listener(publisher):
    if Connected == True :
        global publisher_state
        publisher_state = True
        publisher = Thread(target=publisher_method)
        publisher.start()
    else:
        publisher_state = False
        
def publisher_method():
    while publisher_state:
        Isconnect={"Connected":"On", "timestamp2": datetime.now().isoformat()}
        client.publish(topic="PJM2",payload=json.dumps(Isconnect), qos=1, retain=False)	
        time.sleep(5)
    print ("publishing ending")

while Connected != True:
    time.sleep(5)

client.subscribe("PJM1/#")

try:
    while True:
        time.sleep(1)
        publisher_thread = Thread(target=publisher_method)        
        listener_thread = Thread(target=listener, args=(publisher_thread,))                
        listener_thread.start() 
       
except KeyboardInterrupt:
    print ("exiting")
    GPIO.output(18,GPIO.LOW)
    GPIO.output(23,GPIO.LOW) 
    client.disconnect()
    client.loop_stop()



