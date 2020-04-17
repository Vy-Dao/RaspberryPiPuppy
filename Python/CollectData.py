import sys
import Adafruit_DHT
from gps3 import agps3
import smbus
from pathlib import Path
import csv
import math

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
    
    checkFile = Path('data.csv')
    fieldnames = ['humid','temperature','Altitude','Latitude','Longitude']
    if checkFile.is_file():
        print("File exit")
        with open('data.csv',mode='a') as csv_file:
            writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
            writer.writerow({
                    'humid':humidity,
                    'temperature':temperature,
                    'Altitude':alt,
                    'Latitude':lat,
                    'Longitude':lon})
    else:
        print("File not exit")
        with open('data.csv',mode='w') as csv_file:
            writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
            writer.writerow({
                    'humid':humidity,
                    'temperature':temperature,
                    'Altitude':alt,
                    'Latitude':lat,
                    'Longitude':lon})

