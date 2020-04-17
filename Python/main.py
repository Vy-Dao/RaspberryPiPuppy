from __future__ import print_function
import RPi.GPIO as io
import serial 
from imutils.video import VideoStream
import imutils
import time
import cv2
import os
from time import sleep
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import Adafruit_DHT
from gps3 import agps3
import smbus
from pathlib import Path
import csv
import math
import sys

def clear():
    io.cleanup()

def Forward():
    print("Moving Forward")
    M1En.ChangeDutyCycle(100)
    M2En.ChangeDutyCycle(100)
    io.output(leftMotor_input1,True)
    io.output(leftmotor_input2,False)
    io.output(rightMotor_input1,True)
    io.output(rightMotor_input2,False)

def Backward():
    print("Backrward")
    M1En.ChangeDutyCycle(100)
    M2En.ChangeDutyCycle(100)
    io.output(leftMotor_input1,False)
    io.output(leftmotor_input2,True)
    io.output(rightMotor_input1,False)
    io.output(rightMotor_input2,True)

def TurnRight():
    print("Turn Right")
    M1En.ChangeDutyCycle(100)
    io.output(leftMotor_input1,False)
    io.output(leftmotor_input2,True)

def TurnLeft():
    print("Turn Left")
    M1En.ChangeDutyCycle(100)
    io.output(leftMotor_input1,True)
    io.output(leftmotor_input2,False)

def Stop():
    print("Stop Moving")
    M1En.ChangeDutyCycle(0)
    M2En.ChangeDutyCycle(0)

myMQTT = AWSIoTMQTTClient("")
myMQTT.configureEndpoint("af6uejkaq6p6d-ats.iot.us-east-1.amazonaws.com",8883)
myMQTT.configureCredentials("root.ca.pem", "e30c90799f.private.key", "e30c90799f.cert.pem")
myMQTT.configureOfflinePublishQueueing(-1)
myMQTT.configureDrainingFrequency(2)
myMQTT.configureConnectDisconnectTimeout(10)
myMQTT.configureMQTTOperationTimeout(5)
myMQTT.connect()

#Set-up Breadboard mode
io.setmode(io.BCM)

#Match pin
leftMotor_en = 25
leftMotor_input1 = 24
leftmotor_input2 = 23

rightMotor_en = 17
rightMotor_input1 = 27
rightMotor_input2 = 22



#Set-up pin
io.setup(leftMotor_input1, io.OUT)
io.setup(leftmotor_input2, io.OUT)
io.setup(rightMotor_input1, io.OUT)
io.setup(rightMotor_input2, io.OUT)
io.setup(leftMotor_en, io.OUT)
io.setup(rightMotor_en, io.OUT)

M1En = io.PWM(leftMotor_en,200)
M2En = io.PWM(rightMotor_en,200)

M1En.start(0)
M2En.start(0)

#Reading data from Arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

def readData():
    if ser.in_waiting > 0:
        sleep(0.5)
        line = ser.readline().decode('utf-8')
        return line




def moveDirection (x, y):
    sleep(0.7)
    tmpValue = readData()
    disCenter = float(tmpValue)
    centerRule = True
    if(x<230):
        TurnLeft()
        sleep(0.05)
        Stop()
    elif(x>250):
        TurnRight()
        sleep(0.025)
        Stop()
    elif (x>=230 and x < 250):
        Forward()
        sleep(0.25)
        Stop()

#Initial run camera
print ("Staring the camera. Please wait for 2 seconds")
vs = VideoStream(0).start()
time.sleep(2.0)

# Joycon color
joyconLower = (99, 100, 100)
joyconUpper = (119, 255, 255)


while True:
    sleep(1)
    print("Grab Frame")
    tmpFrame = vs.read()
    tmpFrame = imutils.resize(tmpFrame, width=500)
    tmpFrame = imutils.rotate(tmpFrame, angle=180)
    hsv = cv2.cvtColor(tmpFrame, cv2.COLOR_BGR2HSV)

    print("Create tmpMask")
    tmpMask = cv2.inRange(hsv, joyconLower, joyconUpper)
    tmpMask = cv2.erode(tmpMask, None, iterations=2)
    tmpMask = cv2.dilate(tmpMask, None, iterations=2)

    print("Find Joycon..")
    countsCircle = cv2.findContours(tmpMask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    countsCircle = countsCircle[0] if imutils.is_cv4() else countsCircle[1]
    center = None
    
    if len(countsCircle) > 0:
        print("Find Object")
        circle = max(countsCircle, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(circle)
        MinimumCircle = cv2.moments(circle)
        centerObject = (int(MinimumCircle["m10"] / MinimumCircle["m00"]), int(MinimumCircle["m01"] / MinimumCircle["m00"]))
        tmpValue = readData()
        disCenter = float(tmpValue)
        print(disCenter)
        if(disCenter < 15):
                print("Find Joycon")
                myMQTT.publish("Rasp/Status","Find Joycon",0)
                break
        if radius > 10:
            cv2.circle(tmpFrame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(tmpFrame, center, 5, (0, 0, 255), -1)
            print("Direct movement")
            moveDirection(int(x),int(y))
    
    else:
        Stop()
        TurnLeft()
        sleep(0.25)
        Stop()

    # show the tmpFrame to our screen
    cv2.imshow("tmpFrame", tmpFrame)
    # if [ESC] key is pressed, stop the loop
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

# do a bit of cleanup
print("Find Joycon")
myMQTT.publish("Rasp/Status","Find Joycon",0)
print("\n [INFO] Exiting Program and cleanup stuff \n")
clear()
cv2.destroyAllWindows()
vs.stop()

