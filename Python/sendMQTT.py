from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
import sys
import Adafruit_DHT
from gps3 import agps3
import smbus
from pathlib import Path
import csv
import math


#Setup AWS IoT certificate
myMQTT = AWSIoTMQTTClient("")
myMQTT.configureEndpoint("af6uejkaq6p6d-ats.iot.us-east-1.amazonaws.com",8883)
myMQTT.configureCredentials("root.ca.pem", "e30c90799f.private.key", "e30c90799f.cert.pem")
myMQTT.configureOfflinePublishQueueing(-1)
myMQTT.configureDrainingFrequency(2)
myMQTT.configureConnectDisconnectTimeout(10)
myMQTT.configureMQTTOperationTimeout(5)
myMQTT.connect()

#GPS-Set-up
gps_socket = agps3.GPSDSocket()
data_stream = agps3.DataStream()
gps_socket.connect()
gps_socket.watch()

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11,4)
    temperature = (temperature * 9/5) + 32
    print(humidity)
    print(temperature)
    print()
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            alt = data_stream.alt
            lat = data_stream.lat
            lon = data_stream.lon
        if (lat != "n/a"):
            break
    print('Altitue = ', alt)
    print('Lantitude = ', lat)
    print('Longitude = ', lon)
    print('-------------------')
    tmpString = "The Humidity is: " + str(humidity) + ", The Temperature: " + str(temperature) + ", The Altitude: " + str(alt) + ", The Latitude: " + str(lat) + ", The Longitude: " + str(lon)
    #Connect to AWS
    myMQTT.publish("Rasp/Status",tmpString,0)
    sleep(60)

