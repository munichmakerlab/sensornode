#/bin/python
import serial
import paho.mqtt.client as paho
from threading import Timer

import config

room_open = False

def on_connect(mosq, obj, rc):
	print "[MQTT] Connect with RC " + str(rc)

def on_disconnect(client, userdata, rc):
	print "[MQTT] Disconnected " + str(rc)
	try_reconnect(client)

def on_log(client, userdata, level, buf):
	print "[MQTT] LOG: " + buf

# MQTT reconnect
def try_reconnect(client, time = 60):
	try:
		print "[MQTT] Trying reconnect"
		client.reconnect()
	except:
		print "[MQTT] Reconnect failed. Trying again in " + str(time) + " seconds"
		Timer(time, try_reconnect, [client]).start()

# initialize MQTT
print "[Main] Initializing MQTT Client"
mqttc = paho.Client()
mqttc.username_pw_set(config.broker["user"], config.broker["password"])
mqttc.connect(config.broker["hostname"], config.broker["port"], 60)
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_log = on_log

print "[Main] Initialize serial port"
ser = serial.Serial(config.serial_port, 9600)

# Loop forever
print "[Main] Entering loop"
mqttc.loop_start()

while True:
	message = ser.readline().strip()
	print "[Serial] " + message
	(topic,value) = message.split(";")
	mqttc.publish(config.topic_prefix + topic, value, 0, False)

# Clean up afterwards
print "[Main] Cleanup"
mqttc.disconnect()
